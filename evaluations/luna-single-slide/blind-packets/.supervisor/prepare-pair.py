"""Run only after the production supervisor confirms a PDF is final."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets
import struct
import subprocess

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[2]
PACKETS = ROOT / "blind-packets"
PRIVATE = PACKETS / ".supervisor"
MAPPING = ROOT / "supervisor-mapping.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_chunks(path):
    raw = path.read_bytes()
    offset, names = 8, []
    while offset < len(raw):
        length = struct.unpack(">I", raw[offset:offset + 4])[0]
        names.append(raw[offset + 4:offset + 8].decode("ascii"))
        offset += length + 12
    return names


def anonymize(source, target):
    with Image.open(source) as image:
        assert image.size == (1600, 900), (source, image.size)
        rgb = image.convert("RGB")
        clean = Image.new("RGB", rgb.size)
        clean.paste(rgb)
        clean.save(target, format="PNG")
    with Image.open(target) as output:
        assert not output.info, output.info
        assert ImageChops.difference(rgb, output.convert("RGB")).getbbox() is None
    assert set(png_chunks(target)) <= {"IHDR", "IDAT", "IEND"}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--case", type=int, choices=(1, 2, 3), required=True)
parser.add_argument("--pair-id", choices=("pair-01", "pair-02", "pair-03"))
parser.add_argument("--pdf", help="Final PDF path relative to the evaluation root")
parser.add_argument("--confirmed-final-and-inspected", action="store_true", required=True)
args = parser.parse_args()

sampling_path = ROOT / "sampling.json"
sampling = json.loads(sampling_path.read_text())
page = sampling["selected_pages"][args.case - 1]
pdf = (ROOT / (args.pdf or f"case-{args.case}/outputs/slide.pdf")).resolve()
assert pdf.is_relative_to(ROOT / f"case-{args.case}/outputs"), "PDF must belong to this case's outputs"
reference = ROOT / f"reference-renders/page-{page:03d}-masked.png"
prompt = ROOT / f"case-{args.case}.prompt.txt"
if MAPPING.exists():
    mapping = json.loads(MAPPING.read_text())
else:
    mapping = {"samplingSha256": sha256(sampling_path), "pairs": []}
assert mapping["samplingSha256"] == sha256(sampling_path)
assert not any(item["caseId"] == args.case for item in mapping["pairs"]), "Case already packaged; do not rerandomize"

available = [f"pair-{number:02d}" for number in (1, 2, 3)
             if not any(item["pairId"] == f"pair-{number:02d}" for item in mapping["pairs"])]
pair_id = args.pair_id or secrets.choice(available)
assert pair_id in available, "The requested pair already exists"
packet = PACKETS / pair_id
assert not packet.exists(), "Packet already exists; investigate before replacing it"

pdf_info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
page_count = int(next(line for line in pdf_info.splitlines() if line.startswith("Pages:")).split(":")[1])
assert page_count == 1, "The final PDF must contain exactly one slide"
pdf_hash = sha256(pdf)
pdf_raster = PRIVATE / f"generated-{args.case}-from-final-pdf.png"
subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-singlefile", "-png",
                "-scale-to-x", "1600", "-scale-to-y", "900", str(pdf), str(pdf_raster.with_suffix(""))], check=True)
assert pdf_hash == sha256(pdf), "Final PDF changed while rendering"
png_comparison = {"submittedPngPresent": False}
submitted_png = pdf.with_suffix(".png")
if submitted_png.exists():
    with Image.open(submitted_png) as png, Image.open(pdf_raster) as raster:
        normalized = png.convert("RGB").resize((1600, 900), Image.Resampling.LANCZOS)
        difference = ImageChops.difference(normalized, raster.convert("RGB"))
        png_comparison = {
            "submittedPngPresent": True,
            "submittedPng": str(submitted_png.relative_to(ROOT)),
            "submittedPngSha256": sha256(submitted_png),
            "submittedPngSize": list(png.size),
            "comparisonSize": [1600, 900],
            "meanAbsoluteChannelDifference": ImageStat.Stat(difference).mean,
            "identicalAfterNormalization": difference.getbbox() is None,
            "note": "The packet always uses the final PDF raster; antialiasing and resizing can affect PNG differences.",
        }

brief = prompt.read_text().split("scope / role:\n", 1)[1].strip()
assert "bibliography:" in brief
reference_label = secrets.choice(("A", "B"))
generated_label = "B" if reference_label == "A" else "A"
packet.mkdir()
anonymize(reference, packet / f"{reference_label}.png")
anonymize(pdf_raster, packet / f"{generated_label}.png")
(packet / "brief.txt").write_text("scope / role:\n" + brief + "\n")
assert sorted(path.name for path in packet.iterdir()) == ["A.png", "B.png", "brief.txt"]

record = {
    "pairId": pair_id,
    "caseId": args.case,
    "referencePdfPage": page,
    "referenceLabel": reference_label,
    "generatedLabel": generated_label,
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "finalAndNoExplicitProducerOrPageLabelConfirmed": True,
    "referenceSource": str(reference.relative_to(ROOT)),
    "referenceSourceSha256": sha256(reference),
    "generatedPdf": str(pdf.relative_to(ROOT)),
    "generatedPdfSha256": pdf_hash,
    "generatedPdfInfo": pdf_info,
    "generatedRaster": str(pdf_raster.relative_to(ROOT)),
    "generatedRasterSha256": sha256(pdf_raster),
    "packetSha256": {path.name: sha256(path) for path in sorted(packet.iterdir())},
    "pngMetadataRemoved": True,
    "packetPixelContentUnchanged": True,
    "submittedPngComparison": png_comparison,
}
mapping["pairs"].append(record)
temporary_mapping = MAPPING.with_suffix(".json.tmp")
temporary_mapping.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")
temporary_mapping.replace(MAPPING)
print(json.dumps({"packet": str(packet), "caseId": args.case}, ensure_ascii=False))
