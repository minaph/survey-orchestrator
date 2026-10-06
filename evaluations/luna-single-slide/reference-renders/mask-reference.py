from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[2] / "tmp/MIRU2026_tutorial_share.pdf"
MASKS = {
    102: (1498, 854, 1537, 876),
    18: (1511, 854, 1538, 876),
    20: (1510, 854, 1538, 876),
}

records = []
for page, bounds in MASKS.items():
    original_path = ROOT / f"page-{page:03d}-original.png"
    masked_path = ROOT / f"page-{page:03d}-masked.png"
    original = Image.open(original_path).convert("RGB")
    assert original.size == (1600, 900), original.size
    masked = original.copy()
    masked.paste("white", bounds)
    masked.save(masked_path)
    saved = Image.open(masked_path).convert("RGB")
    difference = ImageChops.difference(original, saved)
    changed_bounds = difference.getbbox()
    outside = difference.copy()
    outside.paste("black", bounds)
    assert outside.getbbox() is None, "Pixels changed outside the page-number mask"
    assert saved.crop(bounds).getextrema() == ((255, 255),) * 3
    records.append({
        "pdfPage": page,
        "original": original_path.name,
        "masked": masked_path.name,
        "size": list(original.size),
        "maskBounds": list(bounds),
        "changedPixelBounds": list(changed_bounds),
        "pixelsOutsideMaskUnchanged": True,
        "originalSha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
        "maskedSha256": hashlib.sha256(masked_path.read_bytes()).hexdigest(),
    })

metadata = {
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "source": "tmp/MIRU2026_tutorial_share.pdf",
    "sourceSha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "coordinateConvention": "PNG pixels, origin top left, [left, top, rightExclusive, bottomExclusive]",
    "purpose": "Mask only the lower-right page number for blind comparison; preserve all content and citations",
    "pages": records,
}
(ROOT / "mask-coordinates.json").write_text(json.dumps(metadata, indent=2) + "\n")
print(json.dumps(metadata, indent=2))
