"""Erzeugt die Transparenzmaske für das Porträt (public/assets/portrait-mask.png).

Die Maske steuert nur die Deckkraft; die Fotopixel bleiben unverändert.
- Person (Silhouette aus scripts/portrait-mask.swift, um DILATE px erweitert): voll deckend
- Hintergrund: läuft weich und transparent in den Seitenhintergrund aus
- Bildränder: immer transparent, außer unten, wo die Person auf der Trennlinie steht

Aufruf: python3 scripts/portrait-fade-mask.py <silhouette.png> <ausgabe.png>
"""

import sys

import numpy as np
from PIL import Image

DILATE = 30  # px Sicherheitsabstand um die Person (Haare, Kanten)
FEATHER = 180  # px Weichheit des Übergangs außerhalb der Person
SCALE = 0.5  # Maske in halber Auflösung (wird vom Browser weich hochskaliert)


def box(img, r):
    pad = np.pad(img, r + 1, mode="edge")
    c = pad.cumsum(0).cumsum(1)
    k = 2 * r + 1
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k])[: img.shape[0], : img.shape[1]] / (k * k)


def blur(img, r, passes=3):
    for _ in range(passes):
        img = box(img, r)
    return img


def smooth_ramp(n, length):
    """0 → 1 über `length` Pixel (smoothstep), danach 1."""
    t = np.clip(np.arange(n) / length, 0, 1)
    return t * t * (3 - 2 * t)


def main(silhouette_path, out_path):
    person = np.asarray(Image.open(silhouette_path).convert("L"), dtype=np.float64) / 255.0 > 0.5
    h, w = person.shape

    grown = box(person.astype(np.float64), DILATE) > 0
    near_person = np.clip(blur(grown.astype(np.float64), FEATHER // 3) * 2, 0, 1)

    # Weiche Ellipse für den umgebenden Raum (Licht, Pflanze), nach außen auslaufend
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx / w - 0.46) / 0.50) ** 2 + ((yy / h - 0.60) / 0.68) ** 2)
    ambient = np.clip((1.0 - d) / 0.45, 0, 1) ** 1.5

    bottom = smooth_ramp(h, h * 0.14)[::-1][:, None]
    top = smooth_ramp(h, 28)[:, None]
    sides = np.minimum(smooth_ramp(w, 120), smooth_ramp(w, 120)[::-1])[None, :]

    alpha = np.maximum(near_person, ambient * bottom) * top * sides
    assert alpha[person & (np.arange(h)[:, None] > 28)].min() > 0.999, "Person nicht voll deckend"

    small = Image.fromarray((alpha * 255 + 0.5).astype(np.uint8)).resize(
        (round(w * SCALE), round(h * SCALE)), Image.Resampling.LANCZOS
    )
    rgba = Image.merge("RGBA", (Image.new("L", small.size, 0),) * 3 + (small,))
    rgba.save(out_path, optimize=True)
    print(f"{out_path}: {small.size[0]}x{small.size[1]}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
