#!/usr/bin/env python3
"""Generates 3 design-direction mockups + app icons for Tagesprotokoll.
Pure-SVG (rendered via cairosvg) so it needs no browser. Fonts are
system stand-ins for the real intended webfonts (noted per design)."""
import cairosvg

W, H = 400, 860
SERIF = "Bitstream Charter, DejaVu Serif, serif"
MONO  = "DejaVu Sans Mono, monospace"
SANS  = "DejaVu Sans, Liberation Sans, sans-serif"

# Shared sample content (same in every design for fair comparison)
ENTRIES = [
    ("14:18", "Heizung im Bad angeschlossen, Druck geprüft."),
    ("13:50", "Material vom Großhandel geholt."),
    ("12:30", "Mittagspause."),
    ("11:05", "Wasserhahn Küche montiert — dicht."),
]
CHIPS = ["Wasserhahn an", "Material geholt", "Pause", "Kunde info."]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def phone_open(bg):
    # rounded screen + clip
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="screen"><rect x="0" y="0" width="{W}" height="{H}" rx="34"/></clipPath></defs>
<rect x="0" y="0" width="{W}" height="{H}" rx="34" fill="{bg}"/>
<g clip-path="url(#screen)">'''


def phone_close():
    return "</g></svg>"


def mic_icon(cx, cy, color, scale=1.0):
    s = scale
    return f'''<g transform="translate({cx},{cy}) scale({s})" fill="{color}">
<rect x="-4.5" y="-11" width="9" height="15" rx="4.5"/>
<path d="M -8 -1 a 8 8 0 0 0 16 0" fill="none" stroke="{color}" stroke-width="2"/>
<line x1="0" y1="7" x2="0" y2="11" stroke="{color}" stroke-width="2"/></g>'''


# ─────────────────────────────────────────────────────────────────────────
# DESIGN A — "Sonnenaufgang"  (warm editorial, refined evolution of current)
# Real fonts: Fraunces (serif) + DM Mono. Accent terracotta.
# ─────────────────────────────────────────────────────────────────────────
def design_a():
    ink, paper, bg = "#1a1612", "#faf7f2", "#f5f0e8"
    accent, muted, line = "#c0392b", "#9a8f82", "#e2ddd6"
    s = phone_open(bg)
    s += f'<rect x="0" y="0" width="{W}" height="200" fill="url(#sun)"/>'
    s += f'''<defs><radialGradient id="sun" cx="82%" cy="0%" r="70%">
<stop offset="0%" stop-color="#c0392b" stop-opacity="0.10"/>
<stop offset="55%" stop-color="#c0392b" stop-opacity="0"/></radialGradient></defs>'''
    # status bar
    s += f'<text x="20" y="26" font-family="{MONO}" font-size="11" fill="{muted}">14:32</text>'
    s += f'<text x="{W-20}" y="26" font-family="{MONO}" font-size="11" fill="{muted}" text-anchor="end">LTE  98%</text>'
    # topbar
    s += f'<rect x="0" y="40" width="{W}" height="62" fill="{ink}"/>'
    s += f'<text x="22" y="78" font-family="{SERIF}" font-size="23" font-weight="bold" fill="{bg}">Tagesprotokoll</text>'
    s += f'<text x="22" y="93" font-family="{MONO}" font-size="9.5" fill="#a89a8a" letter-spacing="1">DI., 22. MAI</text>'
    s += f'<text x="{W-22}" y="84" font-family="{SERIF}" font-style="italic" font-size="26" fill="{accent}" text-anchor="end">14:32</text>'
    # input
    s += f'<rect x="0" y="102" width="{W}" height="64" fill="{paper}"/>'
    s += f'<line x1="0" y1="166" x2="{W}" y2="166" stroke="{line}" stroke-width="1.5"/>'
    s += f'<text x="20" y="141" font-family="{MONO}" font-size="11" fill="{accent}">14:32</text>'
    s += f'<text x="60" y="141" font-family="{MONO}" font-size="13" fill="{muted}">Was ist gerade passiert?</text>'
    s += f'<circle cx="{W-66}" cy="134" r="17" fill="{paper}" stroke="{line}"/>' + mic_icon(W-66, 134, ink, 0.85)
    s += f'<circle cx="{W-26}" cy="134" r="17" fill="{accent}"/><text x="{W-26}" y="140" font-family="{SANS}" font-size="20" fill="#fff" text-anchor="middle">+</text>'
    # chips
    cx = 20
    for c in CHIPS:
        w = 16 + len(c) * 6.4
        s += f'<rect x="{cx}" y="178" width="{w}" height="26" rx="13" fill="{paper}" stroke="{line}"/>'
        s += f'<text x="{cx+w/2}" y="195" font-family="{MONO}" font-size="10.5" fill="{ink}" text-anchor="middle">{esc(c)}</text>'
        cx += w + 8
    # date sep
    s += f'<text x="20" y="232" font-family="{MONO}" font-size="10" fill="{muted}" letter-spacing="1.5">HEUTE</text>'
    s += f'<line x1="70" y1="228" x2="{W-20}" y2="228" stroke="{line}"/>'
    # timeline rail
    railx = 68
    s += f'<line x1="{railx}" y1="250" x2="{railx}" y2="{250+len(ENTRIES)*92-40}" stroke="{line}" stroke-width="1.5"/>'
    y = 262
    for t, txt in ENTRIES:
        s += f'<circle cx="{railx}" cy="{y}" r="4.5" fill="{accent}"/>'
        s += f'<circle cx="{railx}" cy="{y}" r="8" fill="none" stroke="{accent}" stroke-opacity="0.25"/>'
        s += f'<text x="50" y="{y+4}" font-family="{MONO}" font-size="10.5" fill="{accent}" text-anchor="end">{t}</text>'
        # wrap text simply
        words, lines, cur = txt.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) > 28:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        if cur: lines.append(cur)
        yy = y + 4
        for ln in lines:
            s += f'<text x="86" y="{yy}" font-family="{SERIF}" font-size="14.5" fill="{ink}">{esc(ln)}</text>'
            yy += 19
        y += max(92, 40 + len(lines) * 19)
    # bottom bar
    s += f'<rect x="0" y="{H-46}" width="{W}" height="46" fill="{paper}"/>'
    s += f'<line x1="0" y1="{H-46}" x2="{W}" y2="{H-46}" stroke="{line}"/>'
    s += f'<circle cx="20" cy="{H-23}" r="3.5" fill="{accent}"/>'
    s += f'<text x="32" y="{H-19}" font-family="{MONO}" font-size="9.5" fill="{muted}">Bereit · v11</text>'
    s += f'<rect x="{W-150}" y="{H-34}" width="62" height="22" rx="3" fill="none" stroke="{line}"/><text x="{W-119}" y="{H-19}" font-family="{MONO}" font-size="9.5" fill="{muted}" text-anchor="middle">Archiv</text>'
    s += f'<rect x="{W-80}" y="{H-34}" width="62" height="22" rx="3" fill="none" stroke="{line}"/><text x="{W-49}" y="{H-19}" font-family="{MONO}" font-size="9.5" fill="{muted}" text-anchor="middle">Export</text>'
    return s + phone_close()


# ─────────────────────────────────────────────────────────────────────────
# DESIGN B — "Mitternacht"  (dark, focused, technical)
# Real fonts: Fraunces (serif headline) + JetBrains/DM Mono. Accent amber.
# ─────────────────────────────────────────────────────────────────────────
def design_b():
    bg, panel = "#15120d", "#1e1a13"
    text, muted, line = "#ece4d6", "#7d7466", "#2c2720"
    accent = "#e0a44a"
    s = phone_open(bg)
    s += f'''<defs><radialGradient id="glow" cx="50%" cy="0%" r="80%">
<stop offset="0%" stop-color="#e0a44a" stop-opacity="0.12"/>
<stop offset="60%" stop-color="#e0a44a" stop-opacity="0"/></radialGradient></defs>'''
    s += f'<rect x="0" y="0" width="{W}" height="240" fill="url(#glow)"/>'
    s += f'<text x="20" y="26" font-family="{MONO}" font-size="11" fill="{muted}">14:32</text>'
    s += f'<text x="{W-20}" y="26" font-family="{MONO}" font-size="11" fill="{muted}" text-anchor="end">LTE  98%</text>'
    # topbar — minimal, no solid bar, just type
    s += f'<text x="22" y="74" font-family="{SERIF}" font-size="24" font-weight="bold" fill="{text}">Tagesprotokoll</text>'
    s += f'<text x="22" y="91" font-family="{MONO}" font-size="9.5" fill="{muted}" letter-spacing="1.5">DI · 22. MAI 2026</text>'
    s += f'<text x="{W-22}" y="80" font-family="{MONO}" font-size="22" fill="{accent}" text-anchor="end">14:32</text>'
    s += f'<line x1="20" y1="104" x2="{W-20}" y2="104" stroke="{line}"/>'
    # input as a dark panel
    s += f'<rect x="16" y="118" width="{W-32}" height="48" rx="12" fill="{panel}" stroke="{line}"/>'
    s += f'<text x="30" y="147" font-family="{MONO}" font-size="12.5" fill="{muted}">Was ist gerade passiert?</text>'
    s += f'<circle cx="{W-62}" cy="142" r="15" fill="none" stroke="{line}"/>' + mic_icon(W-62, 142, accent, 0.8)
    s += f'<circle cx="{W-28}" cy="142" r="15" fill="{accent}"/><text x="{W-28}" y="148" font-family="{SANS}" font-size="19" fill="#15120d" text-anchor="middle">+</text>'
    # chips
    cx = 20
    for c in CHIPS:
        w = 16 + len(c) * 6.2
        s += f'<rect x="{cx}" y="180" width="{w}" height="25" rx="6" fill="{panel}" stroke="{line}"/>'
        s += f'<text x="{cx+w/2}" y="197" font-family="{MONO}" font-size="10" fill="{accent}" text-anchor="middle">{esc(c)}</text>'
        cx += w + 8
    s += f'<text x="20" y="234" font-family="{MONO}" font-size="9.5" fill="{muted}" letter-spacing="2">// HEUTE</text>'
    # glowing timeline
    railx = 70
    s += f'<line x1="{railx}" y1="250" x2="{railx}" y2="{250+len(ENTRIES)*92-40}" stroke="{line}" stroke-width="1.5"/>'
    y = 262
    for t, txt in ENTRIES:
        s += f'<circle cx="{railx}" cy="{y}" r="11" fill="{accent}" fill-opacity="0.15"/>'
        s += f'<circle cx="{railx}" cy="{y}" r="4" fill="{accent}"/>'
        s += f'<text x="50" y="{y+3}" font-family="{MONO}" font-size="10" fill="{accent}" text-anchor="end">{t}</text>'
        words, lines, cur = txt.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) > 27:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        if cur: lines.append(cur)
        yy = y + 3
        for ln in lines:
            s += f'<text x="88" y="{yy}" font-family="{MONO}" font-size="12.5" fill="{text}">{esc(ln)}</text>'
            yy += 18
        y += max(92, 40 + len(lines) * 18)
    s += f'<rect x="0" y="{H-46}" width="{W}" height="46" fill="{panel}"/>'
    s += f'<circle cx="20" cy="{H-23}" r="3.5" fill="{accent}"/>'
    s += f'<text x="32" y="{H-19}" font-family="{MONO}" font-size="9.5" fill="{muted}">bereit · v11</text>'
    s += f'<rect x="{W-150}" y="{H-34}" width="62" height="22" rx="6" fill="none" stroke="{line}"/><text x="{W-119}" y="{H-19}" font-family="{MONO}" font-size="9.5" fill="{text}" text-anchor="middle">Archiv</text>'
    s += f'<rect x="{W-80}" y="{H-34}" width="62" height="22" rx="6" fill="none" stroke="{line}"/><text x="{W-49}" y="{H-19}" font-family="{MONO}" font-size="9.5" fill="{text}" text-anchor="middle">Export</text>'
    return s + phone_close()


# ─────────────────────────────────────────────────────────────────────────
# DESIGN C — "Karten"  (clean modern, friendly mobile app)
# Real fonts: Inter / system sans. Accent indigo.
# ─────────────────────────────────────────────────────────────────────────
def design_c():
    bg, card = "#f1f3f8", "#ffffff"
    ink, muted, line = "#1f2433", "#8a93a6", "#e6e9f0"
    accent, accent2 = "#4f46e5", "#eef0fe"
    s = phone_open(bg)
    s += f'<text x="20" y="26" font-family="{SANS}" font-size="11" fill="{muted}">14:32</text>'
    s += f'<text x="{W-20}" y="26" font-family="{SANS}" font-size="11" fill="{muted}" text-anchor="end">LTE  98%</text>'
    # header
    s += f'<text x="20" y="68" font-family="{SANS}" font-size="22" font-weight="bold" fill="{ink}">Tagesprotokoll</text>'
    s += f'<text x="20" y="88" font-family="{SANS}" font-size="12" fill="{muted}">Dienstag, 22. Mai · 14:32</text>'
    # input card (rounded, shadow)
    s += f'<rect x="16" y="104" width="{W-32}" height="58" rx="18" fill="{card}" stroke="{line}"/>'
    s += f'<rect x="16" y="104" width="{W-32}" height="58" rx="18" fill="none" stroke="#000" stroke-opacity="0.0"/>'
    s += f'<text x="32" y="138" font-family="{SANS}" font-size="13" fill="{muted}">Was ist gerade passiert?</text>'
    s += f'<circle cx="{W-64}" cy="133" r="16" fill="{accent2}"/>' + mic_icon(W-64, 133, accent, 0.8)
    s += f'<circle cx="{W-28}" cy="133" r="16" fill="{accent}"/><text x="{W-28}" y="139" font-family="{SANS}" font-size="19" fill="#fff" text-anchor="middle">+</text>'
    # chips (pills, accent2 bg)
    cx = 18
    for c in CHIPS:
        w = 18 + len(c) * 6.6
        s += f'<rect x="{cx}" y="176" width="{w}" height="28" rx="14" fill="{accent2}"/>'
        s += f'<text x="{cx+w/2}" y="194" font-family="{SANS}" font-size="11" fill="{accent}" text-anchor="middle">{esc(c)}</text>'
        cx += w + 8
    s += f'<text x="20" y="232" font-family="{SANS}" font-size="11" font-weight="bold" fill="{muted}" letter-spacing="0.5">HEUTE</text>'
    # entry cards
    y = 246
    for t, txt in ENTRIES:
        words, lines, cur = txt.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) > 32:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        if cur: lines.append(cur)
        ch = 30 + len(lines) * 18
        s += f'<rect x="16" y="{y}" width="{W-32}" height="{ch}" rx="16" fill="{card}" stroke="{line}"/>'
        s += f'<rect x="30" y="{y+14}" width="44" height="20" rx="10" fill="{accent2}"/>'
        s += f'<text x="52" y="{y+28}" font-family="{SANS}" font-size="10.5" fill="{accent}" text-anchor="middle">{t}</text>'
        yy = y + 27
        for ln in lines:
            s += f'<text x="86" y="{yy}" font-family="{SANS}" font-size="13" fill="{ink}">{esc(ln)}</text>'
            yy += 18
        y += ch + 12
    # floating bottom nav
    s += f'<rect x="14" y="{H-62}" width="{W-28}" height="46" rx="23" fill="{card}" stroke="{line}"/>'
    s += f'<circle cx="40" cy="{H-39}" r="4" fill="#22c55e"/><text x="54" y="{H-35}" font-family="{SANS}" font-size="11" fill="{muted}">Bereit</text>'
    s += f'<text x="{W-150}" y="{H-35}" font-family="{SANS}" font-size="11.5" fill="{ink}">Archiv</text>'
    s += f'<text x="{W-78}" y="{H-35}" font-family="{SANS}" font-size="11.5" fill="{accent}" font-weight="bold">Export</text>'
    return s + phone_close()


# ─────────────────────────────────────────────────────────────────────────
# APP ICONS — one per design, on a neutral board
# ─────────────────────────────────────────────────────────────────────────
def icons():
    IW, IH = 760, 320
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{IW}" height="{IH}" viewBox="0 0 {IW} {IH}">'
    s += f'<rect width="{IW}" height="{IH}" fill="#eceef2"/>'
    sz, r = 168, 38
    xs = [56, 296, 536]
    labels = ["A · Sonnenaufgang", "B · Mitternacht", "C · Karten"]
    y = 56
    # Icon A: cream tile, serif T, terracotta horizon
    x = xs[0]
    s += f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" rx="{r}" fill="#faf7f2"/>'
    s += f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" rx="{r}" fill="none" stroke="#e2ddd6" stroke-width="2"/>'
    s += f'<text x="{x+sz/2}" y="{y+108}" font-family="{SERIF}" font-size="108" font-weight="bold" fill="#1a1612" text-anchor="middle">T</text>'
    s += f'<rect x="{x+44}" y="{y+128}" width="{sz-88}" height="7" rx="3.5" fill="#c0392b"/>'
    s += f'<circle cx="{x+sz-40}" cy="{y+40}" r="13" fill="#c0392b" fill-opacity="0.85"/>'
    # Icon B: dark tile, amber dot + rail
    x = xs[1]
    s += f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" rx="{r}" fill="#15120d"/>'
    s += f'<line x1="{x+sz/2}" y1="{y+38}" x2="{x+sz/2}" y2="{y+130}" stroke="#2c2720" stroke-width="6"/>'
    s += f'<circle cx="{x+sz/2}" cy="{y+84}" r="34" fill="#e0a44a" fill-opacity="0.18"/>'
    s += f'<circle cx="{x+sz/2}" cy="{y+84}" r="15" fill="#e0a44a"/>'
    s += f'<text x="{x+sz/2}" y="{y+150}" font-family="{MONO}" font-size="20" fill="#ece4d6" text-anchor="middle">protokoll</text>'
    # Icon C: indigo gradient squircle, white doc + check
    x = xs[2]
    s += f'''<defs><linearGradient id="ig" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#6366f1"/><stop offset="100%" stop-color="#4338ca"/></linearGradient></defs>'''
    s += f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" rx="{r}" fill="url(#ig)"/>'
    s += f'<rect x="{x+46}" y="{y+38}" width="76" height="92" rx="12" fill="#fff"/>'
    for i in range(3):
        s += f'<rect x="{x+58}" y="{y+56+i*16}" width="52" height="6" rx="3" fill="#c7cbf5"/>'
    s += f'<circle cx="{x+sz-52}" cy="{y+sz-52}" r="22" fill="#22c55e"/>'
    s += f'<path d="M {x+sz-62} {y+sz-52} l 7 8 l 13 -16" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    for x, lab in zip(xs, labels):
        s += f'<text x="{x+sz/2}" y="{y+sz+34}" font-family="{SANS}" font-size="16" fill="#5a6072" text-anchor="middle">{esc(lab)}</text>'
    return s + "</svg>"


def render(svg, name):
    out = f"png/{name}.png"
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out, output_width=W*2, output_height=H*2)
    print("wrote", out)


import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
open("design_a.svg", "w").write(design_a())
open("design_b.svg", "w").write(design_b())
open("design_c.svg", "w").write(design_c())
open("icons.svg", "w").write(icons())
render(design_a(), "design_a")
render(design_b(), "design_b")
render(design_c(), "design_c")
cairosvg.svg2png(bytestring=icons().encode("utf-8"), write_to="png/icons.png", output_width=1520, output_height=640)
print("wrote png/icons.png")
