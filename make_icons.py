from PIL import Image, ImageDraw, ImageFilter

def make(size):
    SS = 4
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Hintergrund: vertikaler Salbei-Verlauf (warm oben, tiefer unten)
    top = (108, 150, 104)
    bot = (83, 120, 79)
    for y in range(S):
        t = y / S
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        d.line([(0, y), (S, y)], fill=(r, g, b, 255))

    # Warmer gelber Lichtschein oben (weich)
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        [S * 0.08, -S * 0.45, S * 0.92, S * 0.42], fill=(234, 211, 106, 70)
    )
    glow = glow.filter(ImageFilter.GaussianBlur(S * 0.07))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)

    cream = (255, 253, 244, 255)
    cream_soft = (255, 253, 244, 220)
    yellow = (234, 211, 106, 255)

    # Zeitstrahl-Linie
    lx = S * 0.39
    lw = S * 0.013
    d.rounded_rectangle(
        [lx - lw / 2, S * 0.30, lx + lw / 2, S * 0.70],
        radius=lw / 2, fill=(255, 253, 244, 150)
    )

    ys = [0.345, 0.50, 0.655]
    dot_r = S * 0.046
    bar_x = S * 0.50
    bar_h = S * 0.05
    widths = [0.30, 0.235, 0.275]
    dot_cols = [yellow, cream, cream]

    for y, w, c in zip(ys, widths, dot_cols):
        cy = S * y
        # Eintrags-Balken (Text-Andeutung)
        d.rounded_rectangle(
            [bar_x, cy - bar_h / 2, bar_x + S * w, cy + bar_h / 2],
            radius=bar_h / 2, fill=cream_soft
        )
        # Punkt auf dem Strahl (mit dezentem Ring in BG-Farbe)
        ring = dot_r + S * 0.016
        d.ellipse([lx - ring, cy - ring, lx + ring, cy + ring], fill=(95, 130, 90, 255))
        d.ellipse([lx - dot_r, cy - dot_r, lx + dot_r, cy + dot_r], fill=c)

    img = img.resize((size, size), Image.LANCZOS)
    out = Image.new("RGB", (size, size), (95, 130, 90))
    out.paste(img, (0, 0), img)
    return out

for s in (192, 512):
    make(s).save(f"icon-{s}.png")
    print(f"icon-{s}.png geschrieben")
