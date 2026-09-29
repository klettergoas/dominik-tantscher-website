// Erzeugt eine Freistellungsmaske (Graustufen-PNG) für die Hauptperson im Foto.
// Nutzt Apples Vision-Framework (lokal, kein Upload).
// Aufruf: swift scripts/portrait-mask.swift <eingabe.png> <maske.png>
import CoreImage
import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("Aufruf: portrait-mask.swift <eingabe> <maske>") }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])

let handler = VNImageRequestHandler(url: input)
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let result = request.results?.first else { fatalError("Kein Motiv gefunden") }

// Instanz wählen, die die Bildmitte (Person) abdeckt; unscharfe Köpfe im Vordergrund ausschließen
let labels = result.instanceMask
CVPixelBufferLockBaseAddress(labels, .readOnly)
let w = CVPixelBufferGetWidth(labels)
let h = CVPixelBufferGetHeight(labels)
let row = CVPixelBufferGetBytesPerRow(labels)
let base = CVPixelBufferGetBaseAddress(labels)!.assumingMemoryBound(to: UInt8.self)
var counts = [UInt8: Int]()
for y in (h * 3 / 10)..<(h * 6 / 10) {
  for x in (w * 4 / 10)..<(w * 6 / 10) {
    let v = base[y * row + x]
    if v > 0 { counts[v, default: 0] += 1 }
  }
}
CVPixelBufferUnlockBaseAddress(labels, .readOnly)
guard let main = counts.max(by: { $0.value < $1.value })?.key else { fatalError("Person nicht in Bildmitte") }
print("Instanzen: \(result.allInstances.sorted()), gewählt: \(main)")

let mask = try result.generateScaledMaskForImage(forInstances: IndexSet(integer: Int(main)), from: handler)
let ci = CIImage(cvPixelBuffer: mask)
guard let cg = CIContext().createCGImage(ci, from: ci.extent, format: .L8, colorSpace: CGColorSpaceCreateDeviceGray())
else { fatalError("Maske nicht erzeugt") }
let dest = CGImageDestinationCreateWithURL(output as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("Maske: \(cg.width)x\(cg.height)")
