"""Stellt das Porträt frei und erzeugt public/assets/portrait.webp (transparent).

Schritte:
1. Maske aus Apple Vision (scripts/portrait-mask.swift) an den Bildkanten verfeinern (Guided Filter).
2. Randpixel vom hellen Originalhintergrund befreien (Farbsaum entfernen). Pixel,
   die vollständig zur Person gehören, bleiben unverändert.
3. Unteren Bildrand weich auslaufen lassen, auf die Person zuschneiden, als WebP speichern.

Aufruf: python3 scripts/portrait-cutout.py <original.png> <maske.png> <ausgabe.webp>
"""

import sys

import numpy as np
from PIL import Image

ERODE = 5  # px, um die die Vision-Maske verkleinert wird
BAND = 9  # px, Breite der neu berechneten Randzone (Kopf)
SHIRT_ERODE = 3  # px, Verkleinerung der Maske am Oberkörper
HEAD_END = 300  # Bildzeile (Original), ab der der Oberkörper beginnt


def box(img, r):
    """Mittelwertfilter mit Radius r (Summenbild, Randbehandlung durch Normierung)."""
    pad = np.pad(img, ((r + 1, r), (r + 1, r)) + ((0, 0),) * (img.ndim - 2), mode="edge")
    c = pad.cumsum(0).cumsum(1)
    k = 2 * r + 1
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def guided_filter(guide, src, r, eps):
    """Kantenerhaltende Verfeinerung der Maske (He et al.), Graustufen-Guide."""
    mean_i = box(guide, r)
    mean_p = box(src, r)
    cov_ip = box(guide * src, r) - mean_i * mean_p
    var_i = box(guide * guide, r) - mean_i * mean_i
    a = cov_ip / (var_i + eps)
    b = mean_p - a * mean_i
    return box(a, r) * guide + box(b, r)


def blur_normalized(values, weights, r, passes=3):
    """Hintergrundfarbe aus sicheren Hintergrundpixeln in die Randzone hinein schätzen."""
    num = values * weights[..., None]
    den = weights.copy()
    for _ in range(passes):
        num = box(num, r)
        den = box(den, r)
    return num / np.maximum(den, 1e-6)[..., None]


def main(src_path, mask_path, out_path):
    rgb = np.asarray(Image.open(src_path).convert("RGB"), dtype=np.float64) / 255.0
    mask = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float64) / 255.0
    h, w, _ = rgb.shape

    # 1. Maske verfeinern: Die Vision-Maske ist ein paar Pixel zu breit (heller Saum).
    #    Kopf (dunkle Haare/Haut vor hellem Fenster): Deckkraft in der Randzone aus dem
    #    Farbabstand zum Originalhintergrund – erhält feine Haare.
    #    Oberkörper (weißes Hemd vor weißem Hintergrund, dort taugt der Farbabstand nicht):
    #    Vision-Maske leicht verkleinert mit weicher Kante.
    inside = (mask > 0.5).astype(np.float64)
    core = box(inside, ERODE) > 0.999
    band = (box(inside, BAND) > 0) & ~core
    background = blur_normalized(rgb, (box(inside, BAND) == 0).astype(np.float64), r=12)
    dist = np.linalg.norm(rgb - background, axis=2)
    head = np.where(core, 1.0, np.where(band, np.clip((dist - 0.04) / 0.30, 0, 1), 0.0))
    body = box(box((box(inside, SHIRT_ERODE) > 0.999).astype(np.float64), 1), 1)
    t = np.clip((np.arange(h) - HEAD_END) / 60.0, 0, 1)[:, None]  # sanfter Übergang Kopf → Hemd
    alpha = head * (1 - t) + body * t
    alpha = np.clip(guided_filter(rgb @ np.array([0.299, 0.587, 0.114]), alpha, r=2, eps=1e-4), 0, 1)
    alpha[core & (box(core.astype(np.float64), 2) > 0.999)] = 1.0

    # 2. Farbsaum entfernen: C = a*F + (1-a)*B  →  F = (C - (1-a)*B) / a
    #    Nur in der Randzone; alle übrigen Pixel der Person bleiben unverändert.
    edge = (alpha > 0.02) & (alpha < 0.98)
    a = alpha[..., None]
    fg = np.clip((rgb - (1 - a) * background) / np.maximum(a, 1e-3), 0, 1)
    out_rgb = rgb.copy()
    out_rgb[edge] = fg[edge]

    # 3. Zuschnitt auf die Person + weicher Auslauf am unteren Rand
    ys, xs = np.nonzero(alpha > 0.05)
    x0, x1 = max(xs.min() - 60, 0), min(xs.max() + 60, w)
    y0, y1 = max(ys.min() - 40, 0), h
    out_rgb = out_rgb[y0:y1, x0:x1]
    alpha = alpha[y0:y1, x0:x1]
    ch = alpha.shape[0]
    fade_start = int(ch * 0.72)
    ramp = np.ones(ch)
    t = np.linspace(0, 1, ch - fade_start)
    ramp[fade_start:] = 1 - t * t * (3 - 2 * t)  # smoothstep
    alpha = alpha * ramp[:, None]

    rgba = np.dstack([out_rgb, alpha])
    Image.fromarray((rgba * 255 + 0.5).astype(np.uint8)).save(
        out_path, "WEBP", quality=90, alpha_quality=100, method=6
    )
    print(f"{out_path}: {x1 - x0}x{y1 - y0}, Ausschnitt x={x0}..{x1}, y={y0}..{y1}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
