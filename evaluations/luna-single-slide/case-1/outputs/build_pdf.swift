import Foundation
import CoreGraphics
import ImageIO

guard CommandLine.arguments.count == 3 else {
    fputs("usage: swift build_pdf.swift input.png output.pdf\n", stderr)
    exit(2)
}

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
guard let source = CGImageSourceCreateWithURL(inputURL as CFURL, nil),
      let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
    fputs("could not open input image\n", stderr)
    exit(1)
}

// 13.333 × 7.5 in at 72 pt/in. The 1920 × 1080 PNG is placed at 144 ppi.
var mediaBox = CGRect(x: 0, y: 0, width: 960, height: 540)
guard let context = CGContext(outputURL as CFURL, mediaBox: &mediaBox, nil) else {
    fputs("could not create PDF context\n", stderr)
    exit(1)
}
context.beginPDFPage(nil)
context.interpolationQuality = .high
context.draw(image, in: mediaBox)
context.endPDFPage()
context.closePDF()
