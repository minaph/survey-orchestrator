import AppKit
import CoreGraphics
import Foundation

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
guard let nsImage = NSImage(contentsOf: inputURL),
      let cgImage = nsImage.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
  fatalError("Could not load PNG")
}
var mediaBox = CGRect(x: 0, y: 0, width: 960, height: 540)
guard let consumer = CGDataConsumer(url: outputURL as CFURL),
      let context = CGContext(consumer: consumer, mediaBox: &mediaBox, nil) else {
  fatalError("Could not create PDF context")
}
context.beginPDFPage(nil)
context.draw(cgImage, in: mediaBox)
context.endPDFPage()
context.closePDF()
