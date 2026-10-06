# Gallery rendering verification

Generated: 2026-10-07 02:03 JST (2026-10-06T17:03:23.328Z).
Source: `assets/survey-slide-templates.html`.
SHA-256: `80121ba82af29aa84c83b0121cbb23c86cc31881f81ec2ae3ecdeba4233c272d`.
The source hashes before and after rendering match.

## Outputs

- `screen/S*.png`: all 16 stage screenshots in Chrome at viewport 1440 x 1000.
- `mobile-390.png`: Chrome viewport 390 x 844.
- `survey-slide-templates.pdf`: print CSS, 16 pages, background colors included.
- `print/page-*.png`: all 16 PDF pages, rasterized sequentially at 1600 x 900.
- `render-results.json`: per-stage DOM boundary and image loading results.
- `verification-summary.json`: counts, source identity, mobile width, PDF page order.
- `pdfinfo.txt`: PDF metadata and page count.
- `cli-artifacts/`: this run's CLI snapshot.

All screen and print stages have zero descendant left/right/bottom boundary
violations with a 1 CSS pixel tolerance. All 16 image occurrences have
`complete && naturalWidth > 0`. Mobile document and body scroll widths are both
390 CSS pixels. These are automated geometry/load checks; visual quality is
reviewed separately.

## Reproduction

From the repository root, start the server in a separate terminal:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then run CLI commands from this output directory so snapshots remain here:

```sh
cd evaluations/gallery
mkdir -p screen print
shasum -a 256 ../../assets/survey-slide-templates.html > source-before.sha256
playwright-cli -s=gallery-recovery open http://127.0.0.1:8765/assets/survey-slide-templates.html --browser=chrome
playwright-cli -s=gallery-recovery --raw run-code --filename=render-recovery.js > render-results.json
shasum -a 256 ../../assets/survey-slide-templates.html > source-after.sha256
pdfinfo survey-slide-templates.pdf > pdfinfo.txt
pdftoppm -png -scale-to-x 1600 -scale-to-y 900 survey-slide-templates.pdf print/page
playwright-cli -s=gallery-recovery close
```

`render-recovery.js` waits for fonts and image completion, captures stages
sequentially, checks mobile horizontal overflow, and calls `page.pdf` with
`preferCSSPageSize: true` and `printBackground: true`. The script uses this
checkout's absolute output directory; update that path if the checkout moves.
