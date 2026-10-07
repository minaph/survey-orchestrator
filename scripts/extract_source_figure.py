#!/usr/bin/env python3
"""Extract a source figure from an HTML page or a PDF-like document.

The script deliberately requires an explicit image match/index or page/bounds.
It does not guess which figure is scientifically relevant. It downloads the
selected HTML image or renders the selected PDF page region, applies an
optional pixel crop, and writes a small provenance sidecar JSON file.

Examples:
  python extract_source_figure.py html \
    --source https://example.org/article \
    --match 'figure 2|fig2' --crop 20,10,1180,760 \
    --output out/figure-2.png

  python extract_source_figure.py pdf \
    --source paper.pdf --page 4 --bbox 36,42,576,390 --dpi 240 \
    --output out/figure-2.png

For a PPTX, DOCX, ODP, or another format supported by LibreOffice, use the
pdf mode directly; the input is converted to a temporary PDF first.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen


USER_AGENT = "survey-orchestrator/source-figure-extractor/1.0"


def is_url(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "file", "data"}


def web_url_or_none(value: str | None) -> str | None:
    if not value:
        return None
    return value if urlparse(value).scheme in {"http", "https"} else None


def local_path_or_none(value: str | None) -> str | None:
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme == "file":
        return str(Path(unquote(parsed.path)).resolve())
    if not parsed.scheme:
        return str(Path(value).expanduser().resolve())
    return None


def parse_int_box(value: str) -> tuple[int, int, int, int]:
    parts = re.split(r"[,\s]+", value.strip())
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("expected four integers: left,top,right,bottom")
    try:
        result = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box values must be integers") from exc
    if result[2] <= result[0] or result[3] <= result[1]:
        raise argparse.ArgumentTypeError("right/bottom must be greater than left/top")
    return result  # type: ignore[return-value]


def parse_float_box(value: str) -> tuple[float, float, float, float]:
    parts = re.split(r"[,\s]+", value.strip())
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("expected four numbers: x0,y0,x1,y1")
    try:
        result = tuple(float(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box values must be numbers") from exc
    if result[2] <= result[0] or result[3] <= result[1]:
        raise argparse.ArgumentTypeError("x1/y1 must be greater than x0/y0")
    return result  # type: ignore[return-value]


def fetch_bytes_with_final_url(source: str) -> tuple[bytes, str | None]:
    """Read a source and retain a redirect-resolved URL when available."""
    parsed = urlparse(source)
    if parsed.scheme == "data":
        header, payload = source.split(",", 1)
        if ";base64" in header:
            return base64.b64decode(payload), source
        from urllib.parse import unquote as decode_uri

        return decode_uri(payload).encode("utf-8"), source
    if parsed.scheme == "file":
        return Path(unquote(parsed.path)).read_bytes(), source
    if parsed.scheme in {"http", "https"}:
        request = Request(source, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=60) as response:  # noqa: S310 - explicit user source
            return response.read(), response.geturl() or source
    return Path(source).read_bytes(), None


def fetch_bytes(source: str) -> bytes:
    """Read a URL or local path without adding a requests dependency."""
    return fetch_bytes_with_final_url(source)[0]


def load_html(source: str) -> tuple[str, str, str | None, bytes]:
    raw, final_url = fetch_bytes_with_final_url(source)
    base_url = final_url or (source if is_url(source) else Path(source).resolve().as_uri())
    text = raw.decode("utf-8", errors="replace")
    return text, base_url, final_url, raw


def best_src(attrs: dict[str, str]) -> str | None:
    """Prefer full-resolution lazy/srcset candidates over placeholders."""
    value = None
    for key in ("data-full", "data-original", "data-lazy-src", "data-src", "src"):
        if attrs.get(key):
            value = attrs[key]
            break

    candidates: list[tuple[float, str]] = []
    for item in attrs.get("srcset", "").split(","):
        fields = item.strip().split()
        if not fields:
            continue
        score = 0.0
        if len(fields) > 1:
            match = re.match(r"([0-9.]+)(w|x)$", fields[1])
            if match:
                score = float(match.group(1)) * (1.0 if match.group(2) == "w" else 1000.0)
        candidates.append((score, fields[0]))
    if candidates:
        value = max(candidates, key=lambda item: item[0])[1]
    return value


@dataclass
class ImageCandidate:
    index: int
    src: str
    alt: str = ""
    title: str = ""
    figure_id: str = ""
    caption: str = ""
    attrs: dict[str, str] = field(default_factory=dict)

    @property
    def search_text(self) -> str:
        return " ".join(
            value for value in (self.src, self.alt, self.title, self.figure_id, self.caption) if value
        )


class FigureHTMLParser(HTMLParser):
    """Collect img elements and the surrounding figure/caption metadata."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.candidates: list[ImageCandidate] = []
        self.figure_stack: list[dict[str, Any]] = []
        self.caption_depth = 0
        self.caption_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key.lower(): value or "" for key, value in attrs_list}
        tag = tag.lower()
        if tag == "figure":
            self.figure_stack.append(
                {
                    "id": attrs.get("id") or attrs.get("data-figure") or attrs.get("aria-label", ""),
                    "candidate_indexes": [],
                    "caption": "",
                }
            )
        elif tag == "figcaption" and self.figure_stack:
            self.caption_depth += 1
            if self.caption_depth == 1:
                self.caption_parts = []
        elif tag == "img":
            src = best_src(attrs)
            if not src:
                return
            context = self.figure_stack[-1] if self.figure_stack else None
            candidate = ImageCandidate(
                index=len(self.candidates) + 1,
                src=src,
                alt=attrs.get("alt", ""),
                title=attrs.get("title", ""),
                figure_id=context.get("id", "") if context else "",
                attrs=attrs,
            )
            self.candidates.append(candidate)
            if context is not None:
                context["candidate_indexes"].append(candidate.index - 1)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "figcaption" and self.caption_depth:
            self.caption_depth -= 1
            if self.caption_depth == 0 and self.figure_stack:
                self.figure_stack[-1]["caption"] = " ".join("".join(self.caption_parts).split())
        elif tag == "figure" and self.figure_stack:
            context = self.figure_stack.pop()
            caption = context.get("caption", "")
            for index in context.get("candidate_indexes", []):
                self.candidates[index].caption = caption

    def handle_data(self, data: str) -> None:
        if self.caption_depth:
            self.caption_parts.append(data)


def resolve_image_url(base_url: str, src: str) -> str:
    return urljoin(base_url, src)


def choose_candidate(
    candidates: list[ImageCandidate], index: int | None, pattern: str | None
) -> ImageCandidate:
    if not candidates:
        raise RuntimeError("no <img> candidates were found in the HTML")
    if index is not None and pattern is not None:
        raise RuntimeError("use either --index or --match, not both")
    if index is not None:
        if index < 1 or index > len(candidates):
            raise RuntimeError(f"--index must be between 1 and {len(candidates)}")
        return candidates[index - 1]
    if pattern is not None:
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as exc:
            raise RuntimeError(f"invalid --match regular expression: {exc}") from exc
        matches = [candidate for candidate in candidates if regex.search(candidate.search_text)]
        if len(matches) != 1:
            details = "\n".join(
                f"  {candidate.index}: {candidate.search_text[:180]}" for candidate in matches or candidates
            )
            raise RuntimeError(
                f"--match selected {len(matches)} images; refine it or use --index.\n{details}"
            )
        return matches[0]
    raise RuntimeError("specify --index or --match so the selected figure is auditable")


def crop_image(image, box: tuple[int, int, int, int] | None):
    if box is None:
        return image
    width, height = image.size
    if box[0] < 0 or box[1] < 0 or box[2] > width or box[3] > height:
        raise RuntimeError(f"pixel crop {box} is outside image bounds {width}x{height}")
    return image.crop(box)


def save_image(image, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {".jpg", ".jpeg"}:
        image.convert("RGB").save(output, quality=95, optimize=True)
    else:
        image.save(output, optimize=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mime_type(value: str | None, fallback: str | None = None) -> str | None:
    guessed, _ = mimetypes.guess_type(value or "")
    return guessed or fallback


def metadata_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--asset-id", help="optional asset-ledger identifier; defaults to output stem")
    parser.add_argument("--visual-id", help="claim-bearing visual identifier for the per-visual sidecar join")
    parser.add_argument("--generation-id", help="optional declaration/generation identifier used for cross-artifact joins")
    parser.add_argument("--figure-id", help="optional G4-V figure-candidate identifier")
    parser.add_argument("--source-id", help="optional audit-plane source identifier")
    parser.add_argument(
        "--claim-id",
        action="append",
        default=[],
        help="claim identifier linked to this figure; repeat for multiple claims",
    )
    parser.add_argument(
        "--canonical-url-or-doi",
        help="optional canonical article URL or DOI; do not infer one silently",
    )
    parser.add_argument(
        "--rights-basis",
        help="optional manually supplied reuse basis, e.g. article32_quotation, open_licence, permission, public_domain",
    )
    parser.add_argument(
        "--license-status",
        default="not_applicable",
        help="licence state when relevant; use not_applicable for quotation-based reuse",
    )
    parser.add_argument(
        "--fidelity-status",
        default="pending",
        choices=("pending", "passed", "blocked", "not_required", "not_applicable"),
        help="manual/source-fidelity review state; default pending",
    )


def transformation_history(
    *, selected: str, crop: tuple[int, int, int, int] | None, autocontrast: bool,
    conversion: dict[str, str] | None = None,
) -> list[str]:
    history = [selected]
    if conversion:
        history.append(f"convert to PDF with {conversion.get('tool', 'not reported')} {conversion.get('version', '')}".strip())
    if crop:
        history.append(f"pixel crop {','.join(str(value) for value in crop)}")
    if autocontrast:
        history.append("autocontrast")
    history.append("write output")
    return history


def write_manifest(output: Path, manifest_path: Path | None, payload: dict[str, Any]) -> None:
    if manifest_path is None:
        return
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def html_command(args: argparse.Namespace) -> int:
    from PIL import Image, ImageOps

    text, base_url, final_source_url, source_bytes = load_html(args.source)
    parser = FigureHTMLParser()
    parser.feed(text)
    if args.list:
        for candidate in parser.candidates:
            print(
                json.dumps(
                    {
                        "index": candidate.index,
                        "src": candidate.src,
                        "alt": candidate.alt,
                        "figure_id": candidate.figure_id,
                        "caption": candidate.caption,
                    },
                    ensure_ascii=False,
                )
            )
        return 0
    if not args.output:
        raise RuntimeError("--output is required unless --list is used")
    candidate = choose_candidate(parser.candidates, args.index, args.match)
    image_url = resolve_image_url(base_url, candidate.src)
    image_bytes, final_image_url = fetch_bytes_with_final_url(image_url)
    image_file = Image.open(BytesIO(image_bytes))
    source_mime = Image.MIME.get(image_file.format or "") or mime_type(image_url, "application/octet-stream")
    image = image_file.convert("RGB")
    source_size = image.size
    image = crop_image(image, args.crop)
    if args.autocontrast:
        image = ImageOps.autocontrast(image)
    output = Path(args.output)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    figure_locator = candidate.figure_id or f"HTML image candidate {candidate.index}"
    source_page_web_url = web_url_or_none(args.source)
    image_web_url = web_url_or_none(image_url)
    final_image_web_url = web_url_or_none(final_image_url or image_url)
    save_image(image, output)
    manifest = {
        "asset_id": args.asset_id or output.stem,
        "tool": "extract_source_figure.py",
        "retrieved_at": retrieved_at,
        "retrieval_date": retrieved_at,
        "mode": "html",
        "acquisition_mode": "html",
        "visual_id": args.visual_id,
        "generation_id": args.generation_id,
        "figure_id": args.figure_id,
        "source_id": args.source_id,
        "claim_ids": args.claim_id,
        "asset_role": "source_cutout",
        "review_only": True,
        "fidelity_status": args.fidelity_status,
        "canonical_url_or_doi": args.canonical_url_or_doi,
        "source_url_or_doi": args.canonical_url_or_doi or source_page_web_url,
        "retrieved_url": image_web_url,
        "final_url": final_image_web_url,
        "source_page_url": source_page_web_url,
        "source_page_final_url": web_url_or_none(final_source_url),
        "local_source_path": local_path_or_none(args.source),
        "local_image_path": local_path_or_none(image_url),
        "source_page_sha256": sha256_bytes(source_bytes),
        "source_sha256": sha256_bytes(image_bytes),
        "source_hash_basis": "local_image_file" if local_path_or_none(image_url) else "acquired_image_bytes",
        "rights_basis": args.rights_basis or "not provided",
        "license_status": args.license_status,
        "figure_or_page_locator": figure_locator,
        "asset_url": final_image_web_url,
        "source_html": args.source,
        "image_url": image_web_url,
        "candidate": {
            "index": candidate.index,
            "alt": candidate.alt,
            "figure_id": candidate.figure_id,
            "caption": candidate.caption,
        },
        "source_image_size_px": list(source_size),
        "source_mime_type": source_mime,
        "mime_type": source_mime,
        "pixel_crop": list(args.crop) if args.crop else None,
        "crop_spec": {
            "pdf_bbox_pt": None,
            "pixel_crop": list(args.crop) if args.crop else None,
        },
        "output": str(output),
        "output_size_px": list(image.size),
        "output_dimensions": list(image.size),
        "output_mime_type": mime_type(str(output), "image/png"),
        "output_sha256": sha256(output),
        "transformation_history": transformation_history(
            selected=f"select HTML image candidate {candidate.index}",
            crop=args.crop,
            autocontrast=args.autocontrast,
        ),
    }
    manifest_path = None if args.no_manifest else Path(args.manifest or output.with_suffix(".json"))
    write_manifest(output, manifest_path, manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def find_office() -> str | None:
    return shutil.which("libreoffice") or shutil.which("soffice")


def pdf_path_for_source(
    source: str, stack: ExitStack
) -> tuple[Path, str | None, dict[str, str] | None, str | None, str]:
    """Materialize a local PDF, converting common PDF-capable formats when needed."""
    converted_from: str | None = None
    conversion: dict[str, str] | None = None
    final_url: str | None = None
    source_sha256: str
    if is_url(source):
        temp_dir = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="source-figure-")))
        suffix = Path(urlparse(source).path).suffix or ".bin"
        source_path = temp_dir / f"input{suffix}"
        source_bytes, final_url = fetch_bytes_with_final_url(source)
        source_path.write_bytes(source_bytes)
        source_sha256 = sha256_bytes(source_bytes)
    else:
        source_path = Path(source).expanduser().resolve()
        source_sha256 = sha256(source_path)
    # Many repository PDF endpoints (for example /pdf/<id>) have no .pdf
    # suffix, so inspect the magic bytes as well as the filename.
    with source_path.open("rb") as stream:
        magic = stream.read(5)
    if source_path.suffix.lower() == ".pdf" or magic == b"%PDF-":
        return source_path, converted_from, conversion, final_url, source_sha256
    office = find_office()
    if not office:
        raise RuntimeError(
            f"{source_path.suffix or 'this format'} is not PDF; install LibreOffice/soffice or convert it first"
        )
    version_result = subprocess.run([office, "--version"], capture_output=True, text=True, check=False)
    version_text = (version_result.stdout or version_result.stderr).strip()
    office_version = version_text.splitlines()[0] if version_text else "not reported"
    temp_dir = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="source-figure-pdf-")))
    command = [office, "--headless", "--convert-to", "pdf", "--outdir", str(temp_dir), str(source_path)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    converted = temp_dir / f"{source_path.stem}.pdf"
    if result.returncode != 0 or not converted.exists():
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"LibreOffice conversion failed: {detail or 'no PDF was produced'}")
    converted_from = source if is_url(source) else str(source_path)
    conversion = {"tool": Path(office).name, "version": office_version}
    return converted, converted_from, conversion, final_url, source_sha256


def pdf_command(args: argparse.Namespace) -> int:
    from PIL import Image, ImageOps

    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "pdf mode requires PyMuPDF (fitz); run `devbox run setup` then "
            "`devbox run python scripts/extract_source_figure.py ...`; "
            "see docs/evaluation-environment.md"
        ) from exc
    if not args.output:
        raise RuntimeError("--output is required")
    if args.page < 1:
        raise RuntimeError("--page is 1-based and must be at least 1")
    if args.dpi <= 0:
        raise RuntimeError("--dpi must be positive")
    if args.bbox is None and args.crop is None:
        raise RuntimeError("provide --bbox or --crop; an untrimmed full-page output is not a figure extract")

    with ExitStack() as stack:
        pdf_path, converted_from, conversion, final_source_url, source_sha256 = pdf_path_for_source(args.source, stack)
        doc = fitz.open(str(pdf_path))
        if args.page > len(doc):
            raise RuntimeError(f"--page {args.page} exceeds the document's {len(doc)} pages")
        page = doc[args.page - 1]
        page_rect = page.rect
        clip = fitz.Rect(args.bbox) if args.bbox else page_rect
        if not page_rect.contains(clip):
            raise RuntimeError(f"--bbox {tuple(args.bbox)} is outside page bounds {tuple(page_rect)}")
        scale = args.dpi / 72.0
        pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip, alpha=False)
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        rendered_size = image.size
        image = crop_image(image, args.crop)
        if args.autocontrast:
            image = ImageOps.autocontrast(image)
        output = Path(args.output)
        retrieved_at = datetime.now(timezone.utc).isoformat()
        bbox_locator = ",".join(str(value) for value in args.bbox) if args.bbox else "none"
        source_web_url = web_url_or_none(args.source)
        final_web_url = web_url_or_none(final_source_url)
        save_image(image, output)
        manifest = {
            "asset_id": args.asset_id or output.stem,
            "tool": "extract_source_figure.py",
            "retrieved_at": retrieved_at,
            "retrieval_date": retrieved_at,
            "mode": "pdf",
            "acquisition_mode": "pdf-render",
            "visual_id": args.visual_id,
            "generation_id": args.generation_id,
            "figure_id": args.figure_id,
            "source_id": args.source_id,
            "claim_ids": args.claim_id,
            "asset_role": "source_cutout",
            "review_only": True,
            "fidelity_status": args.fidelity_status,
            "canonical_url_or_doi": args.canonical_url_or_doi,
            "source_url_or_doi": args.canonical_url_or_doi or source_web_url,
            "retrieved_url": source_web_url,
            "final_url": final_web_url,
            "local_source_path": local_path_or_none(args.source),
            "source_sha256": source_sha256,
            "source_hash_basis": "local_source_file" if not is_url(args.source) else "acquired_source_bytes",
            "rights_basis": args.rights_basis or "not provided",
            "license_status": args.license_status,
            "figure_or_page_locator": f"PDF page {args.page}; bbox {bbox_locator}",
            "asset_url": final_web_url,
            "source_mime_type": "application/pdf",
            "mime_type": "application/pdf",
            "source": args.source,
            "converted_from": converted_from,
            "conversion": conversion,
            "page": args.page,
            "page_count": len(doc),
            "page_size_pt": [page_rect.width, page_rect.height],
            "pdf_bbox_pt": list(args.bbox) if args.bbox else None,
            "render_dpi": args.dpi,
            "rendered_size_px": list(rendered_size),
            "pixel_crop": list(args.crop) if args.crop else None,
            "crop_spec": {
                "pdf_bbox_pt": list(args.bbox) if args.bbox else None,
                "pixel_crop": list(args.crop) if args.crop else None,
            },
            "output": str(output),
            "output_size_px": list(image.size),
            "output_dimensions": list(image.size),
            "output_mime_type": mime_type(str(output), "image/png"),
            "output_sha256": sha256(output),
            "transformation_history": transformation_history(
                selected=f"render PDF page {args.page}",
                crop=args.crop,
                autocontrast=args.autocontrast,
                conversion=conversion,
            ),
        }
        manifest_path = None if args.no_manifest else Path(args.manifest or output.with_suffix(".json"))
        write_manifest(output, manifest_path, manifest)
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    html = subparsers.add_parser("html", help="download an image referenced by HTML")
    html.add_argument("--source", required=True, help="HTML URL or local HTML file")
    selector = html.add_mutually_exclusive_group()
    selector.add_argument("--index", type=int, help="1-based image candidate index")
    selector.add_argument("--match", help="case-insensitive regex over image URL, alt, figure id, and caption")
    html.add_argument("--list", action="store_true", help="list candidates instead of extracting")
    html.add_argument("--crop", type=parse_int_box, help="pixel crop: left,top,right,bottom")
    html.add_argument("--autocontrast", action="store_true")
    html.add_argument("--output", help="output image path")
    html.add_argument("--manifest", help="optional provenance JSON path")
    html.add_argument(
        "--no-manifest",
        action="store_true",
        help="suppress the provenance JSON sidecar for exploratory output only",
    )
    metadata_args(html)
    html.set_defaults(func=html_command)

    pdf = subparsers.add_parser("pdf", help="render and crop a PDF or PDF-convertible file")
    pdf.add_argument("--source", required=True, help="PDF/file URL or local PDF, PPTX, DOCX, ODP, etc.")
    pdf.add_argument("--page", type=int, required=True, help="1-based page/slide after conversion")
    pdf.add_argument("--bbox", type=parse_float_box, help="PDF points: x0,y0,x1,y1; origin is top-left")
    pdf.add_argument("--dpi", type=int, default=240, help="rendering resolution; default 240")
    pdf.add_argument("--crop", type=parse_int_box, help="pixel crop after rendering: left,top,right,bottom")
    pdf.add_argument("--autocontrast", action="store_true")
    pdf.add_argument("--output", required=True, help="output image path")
    pdf.add_argument("--manifest", help="optional provenance JSON path")
    pdf.add_argument(
        "--no-manifest",
        action="store_true",
        help="suppress the provenance JSON sidecar for exploratory output only",
    )
    metadata_args(pdf)
    pdf.set_defaults(func=pdf_command)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # make CLI failures concise and actionable
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
