#!/usr/bin/env python3
"""
Build PNG overlay set for the V3 intro video.

Output: ../overlays/  (under website-intro/)
  - slide-0_cover.png                 — single PNG, holding card
  - slide-1_hook/                     — 180-frame sequence (6s @ 30fps), counter 1→20 + filling bar
      frame_0001.png ... frame_0180.png
      final.png                       — copy of the end state, standalone
  - slide-2_stairs/                   — 3 keyframes for crossfade in DaVinci
      state-1_estudiamos.png
      state-2_est_ident.png
      state-3_all.png
      final.png                       — same as state-3
  - slide-3_proof.png
  - slide-4_diferencia.png
  - slide-5_cta.png

Design: 1920x1080 RGBA, fully transparent background. Content positioned on the
LEFT third of the frame so a centered talking-head subject (T7) is not covered.
Brand colors inverted for white-background readability:
  - text:     Midnight  #0C1A2E
  - accent:   SkyBlue   #0EA5E9
  - muted:    #5A6B85
  - whatsapp: #25D366

Run from this folder:   python3 build_overlays.py
"""

import os
import math
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ─── Paths ─────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "overlays"     # /srv/Nexostrat/operations/marketing/website-intro/overlays/

# ─── Canvas ────────────────────────────────────────────────────────────────
W, H = 1920, 1080
LEFT = 80      # left margin

# ─── Colors (RGBA) ─────────────────────────────────────────────────────────
MIDNIGHT = (12, 26, 46, 255)
SKY      = (14, 165, 233, 255)
MUTED    = (90, 107, 133, 255)
WHATSAPP = (37, 211, 102, 255)
INK_SOFT = (12, 26, 46, 30)        # very translucent navy for bar tracks

# ─── Fonts ─────────────────────────────────────────────────────────────────
INTER_DIR = Path("/usr/share/fonts/opentype/inter")
FONT_REG   = str(INTER_DIR / "Inter-Regular.otf")
FONT_MED   = str(INTER_DIR / "Inter-Medium.otf")
FONT_SEMI  = str(INTER_DIR / "Inter-SemiBold.otf")
FONT_BOLD  = str(INTER_DIR / "Inter-Bold.otf")
FONT_XBOLD = str(INTER_DIR / "Inter-ExtraBold.otf")
FONT_BLACK = str(INTER_DIR / "Inter-Black.otf")

def f(path, size):
    return ImageFont.truetype(path, size)

# ─── Helpers ───────────────────────────────────────────────────────────────
def canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def draw_tracked_text(draw, xy, text, font, fill, tracking_em=0.18):
    """Draw text with letter-spacing (since PIL doesn't natively support it).
    tracking_em is fraction of font-size added between each character."""
    x, y = xy
    spacing_px = int(font.size * tracking_em)
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = font.getbbox(ch)
        char_w = bbox[2] - bbox[0]
        x += char_w + spacing_px

def rounded_pill(draw, bbox, fill=None, outline=None, width=2, radius=None):
    x0, y0, x1, y1 = bbox
    if radius is None:
        radius = (y1 - y0) // 2
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def pill_with_text(img, draw, center_xy, text, font, fill_text=MIDNIGHT, fill_bg=None,
                   outline=SKY, outline_w=3, pad_x=44, pad_y=22, radius=None):
    """Draw a pill with text centered. Returns its bounding box."""
    bbox_t = font.getbbox(text)
    tw = bbox_t[2] - bbox_t[0]
    th = bbox_t[3] - bbox_t[1]
    cx, cy = center_xy
    x0 = cx - tw // 2 - pad_x
    x1 = cx + tw // 2 + pad_x
    y0 = cy - th // 2 - pad_y
    y1 = cy + th // 2 + pad_y
    rounded_pill(draw, (x0, y0, x1, y1), fill=fill_bg, outline=outline,
                 width=outline_w, radius=radius)
    # Draw text centered in pill
    draw.text((cx - tw // 2 - bbox_t[0], cy - th // 2 - bbox_t[1]),
              text, font=font, fill=fill_text)
    return (x0, y0, x1, y1)

def with_alpha(rgb, a):
    return (rgb[0], rgb[1], rgb[2], a)

def save(img, path):
    path = str(path)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)

# ─── Slide 0 — Cover (logo holder) ─────────────────────────────────────────
def render_slide0():
    img = canvas()
    d = ImageDraw.Draw(img)
    # Wordmark — recreate type-only "nexostrat" with the brand's cyan pill on "strat"
    # Position left
    base_y = 460
    # "nexo" in Midnight
    font_logo = f(FONT_BLACK, 140)
    nexo = "nexo"
    bbox_n = font_logo.getbbox(nexo)
    nx, ny = LEFT, base_y
    d.text((nx, ny), nexo, font=font_logo, fill=MIDNIGHT)
    nw = bbox_n[2] - bbox_n[0]
    # "strat" pill in SkyBlue with white text
    strat = "strat"
    bbox_s = font_logo.getbbox(strat)
    sw = bbox_s[2] - bbox_s[0]
    pill_x0 = nx + nw + 12
    pill_y0 = ny + 4
    pill_x1 = pill_x0 + sw + 60
    pill_y1 = pill_y0 + (bbox_s[3] - bbox_s[1]) + 36
    d.rounded_rectangle((pill_x0, pill_y0, pill_x1, pill_y1), radius=32, fill=SKY)
    d.text((pill_x0 + 30 - bbox_s[0], pill_y0 + 18 - bbox_s[1]), strat,
           font=font_logo, fill=(240, 251, 255, 255))
    # URL below
    font_url = f(FONT_MED, 36)
    d.text((LEFT + 6, pill_y1 + 36), "nexostrat.com", font=font_url, fill=MUTED)
    return img

# ─── Slide 1 — Hook (animated 1→20 counter + progress bar) ─────────────────
def render_slide1(counter_value, progress_pct):
    img = canvas()
    d = ImageDraw.Draw(img)

    # Eyebrow
    draw_tracked_text(d, (LEFT, 180), "CADA SEMANA",
                      f(FONT_BOLD, 28), MUTED, tracking_em=0.22)

    # Headline (two lines)
    font_h = f(FONT_BOLD, 72)
    d.text((LEFT, 235), "¿Cuántas horas", font=font_h, fill=MIDNIGHT)
    d.text((LEFT, 325), "pierde tu equipo?", font=font_h, fill=MIDNIGHT)

    # Hero number
    font_num = f(FONT_BLACK, 280)
    num_str = str(counter_value)
    bbox_num = font_num.getbbox(num_str)
    nx, ny = LEFT, 470
    d.text((nx, ny), num_str, font=font_num, fill=SKY)
    num_w = bbox_num[2] - bbox_num[0]

    # "hrs" unit
    font_unit = f(FONT_SEMI, 64)
    d.text((nx + num_w + 28, ny + 130), "hrs", font=font_unit, fill=MIDNIGHT)

    # Sub-label
    font_sub = f(FONT_MED, 36)
    d.text((LEFT, 800), "en tareas repetitivas", font=font_sub, fill=MIDNIGHT)

    # Progress bar
    bar_x0 = LEFT
    bar_y0 = 880
    bar_w = 620
    bar_h = 14
    d.rounded_rectangle((bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h),
                        radius=bar_h // 2, fill=INK_SOFT)
    fill_w = max(0, int(bar_w * progress_pct / 100))
    if fill_w > 0:
        d.rounded_rectangle((bar_x0, bar_y0, bar_x0 + fill_w, bar_y0 + bar_h),
                            radius=bar_h // 2, fill=SKY)
    return img

def gen_slide1_sequence(out_dir, fps=30, duration_s=6.0):
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = int(round(fps * duration_s))
    for i in range(n):
        t = i / max(1, n - 1)            # 0 → 1 inclusive
        eased = 1 - (1 - t) ** 1.5       # match the deck's eased-out
        value = round(1 + (20 - 1) * eased)
        progress = t * 100
        img = render_slide1(value, progress)
        save(img, out_dir / f"frame_{i + 1:04d}.png")
    # Hold "20" final state as a standalone
    save(render_slide1(20, 100), out_dir / "final.png")
    return n

# ─── Slide 2 — Solution stairs (4 keyframes for crossfade) ─────────────────
PILL_ORDER = ("estudiamos", "identificamos", "disenamos", "implementamos")
PILL_LABEL = {
    "estudiamos":    "Estudiamos",
    "identificamos": "Identificamos",
    "disenamos":     "Diseñamos",
    "implementamos": "Implementamos",
}

def render_slide2(visible=PILL_ORDER):
    """visible: tuple of which pills are revealed (in any order)."""
    img = canvas()
    d = ImageDraw.Draw(img)

    # Eyebrow
    draw_tracked_text(d, (LEFT, 180), "EN NEXOSTRAT",
                      f(FONT_BOLD, 28), MUTED, tracking_em=0.22)

    # Pill style + positions — 4-step staircase rising up-right.
    # Centers chosen so even the widest pill ("Identificamos"/"Implementamos")
    # right edge stays clear of Ricardo's left shoulder (~x=700 in 1920 frame).
    font_pill = f(FONT_BOLD, 52)
    pos = {
        "estudiamos":    (LEFT + 150, 830),   # bottom-left
        "identificamos": (LEFT + 270, 660),
        "disenamos":     (LEFT + 380, 490),
        "implementamos": (LEFT + 480, 320),   # top-right
    }

    # Pills (drawn in fixed visual order so overlap is consistent)
    for name in PILL_ORDER:
        if name in visible:
            pill_with_text(img, d, pos[name], PILL_LABEL[name], font_pill,
                           fill_text=MIDNIGHT, fill_bg=with_alpha(SKY[:3], 28),
                           outline=SKY, outline_w=4, pad_x=38, pad_y=20)
    return img

def gen_slide2_keyframes(out_dir):
    """Render 4 progressive states for DaVinci to crossfade between."""
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    save(render_slide2(("estudiamos",)),
         out_dir / "state-1_estudiamos.png")
    save(render_slide2(("estudiamos", "identificamos")),
         out_dir / "state-2_est_ident.png")
    save(render_slide2(("estudiamos", "identificamos", "disenamos")),
         out_dir / "state-3_plus_disena.png")
    save(render_slide2(PILL_ORDER),
         out_dir / "state-4_all.png")
    save(render_slide2(PILL_ORDER),
         out_dir / "final.png")

# ─── Slide 3 — Proof (8–20 hrs hero) ───────────────────────────────────────
def render_slide3():
    img = canvas()
    d = ImageDraw.Draw(img)

    draw_tracked_text(d, (LEFT, 180), "LA META",
                      f(FONT_BOLD, 28), MUTED, tracking_em=0.22)

    # Hero number "8–20"
    font_num = f(FONT_BLACK, 280)
    s = "8–20"
    d.text((LEFT, 280), s, font=font_num, fill=SKY)

    # Big "hrs"
    font_hrs = f(FONT_SEMI, 64)
    bbox_n = font_num.getbbox(s)
    nw = bbox_n[2] - bbox_n[0]
    d.text((LEFT + nw + 32, 410), "hrs", font=font_hrs, fill=MIDNIGHT)

    # Sub
    font_sub = f(FONT_MED, 44)
    d.text((LEFT, 600), "horas recuperadas / semana",
           font=font_sub, fill=MIDNIGHT)

    # Foot
    draw_tracked_text(d, (LEFT, 700), "DECIDIR · VENDER · CRECER",
                      f(FONT_SEMI, 26), MUTED, tracking_em=0.20)
    return img

# ─── Slide 4 — Diferencia ──────────────────────────────────────────────────
def render_slide4():
    img = canvas()
    d = ImageDraw.Draw(img)

    draw_tracked_text(d, (LEFT, 200), "DIFERENCIA",
                      f(FONT_BOLD, 28), MUTED, tracking_em=0.22)

    # "Hecho" + cyan "a tu medida."
    font_h = f(FONT_BOLD, 96)
    d.text((LEFT, 280), "Hecho", font=font_h, fill=MIDNIGHT)
    d.text((LEFT, 400), "a tu medida.", font=font_h, fill=SKY)

    # Sub
    draw_tracked_text(d, (LEFT, 580), "SIN PLANTILLAS",
                      f(FONT_BOLD, 26), MIDNIGHT, tracking_em=0.18)
    draw_tracked_text(d, (LEFT, 625), "SOBRE CÓMO FUNCIONA TU NEGOCIO",
                      f(FONT_MED, 24), MUTED, tracking_em=0.16)
    return img

# ─── Slide 5 — CTA (WhatsApp) ──────────────────────────────────────────────
def render_slide5():
    img = canvas()
    d = ImageDraw.Draw(img)

    draw_tracked_text(d, (LEFT, 220), "HABLEMOS",
                      f(FONT_BOLD, 28), MUTED, tracking_em=0.22)

    # WhatsApp icon — official brand logo from assets/whatsapp.png
    wa_logo = Image.open(HERE / "assets" / "whatsapp.png").convert("RGBA")
    isize = 160                                    # rendered size on canvas
    wa_logo = wa_logo.resize((isize, isize), Image.LANCZOS)
    ix0, iy0 = LEFT, 285                           # left edge anchor
    img.alpha_composite(wa_logo, (ix0, iy0))

    # Number — vertically centered against the larger icon
    font_num = f(FONT_BOLD, 84)
    num_y = iy0 + (isize - 84) // 2 - 6     # baseline-ish align with icon center
    d.text((LEFT + isize + 40, num_y), "+57 333 286 3969",
           font=font_num, fill=MIDNIGHT)

    # Sub
    draw_tracked_text(d, (LEFT, 540), "30 MINUTOS  ·  SIN COSTO",
                      f(FONT_BOLD, 28), MIDNIGHT, tracking_em=0.18)
    return img

# ─── Build everything ──────────────────────────────────────────────────────
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Writing to: {OUT}")

    # Static slides
    save(render_slide0(), OUT / "slide-0_cover.png")
    print(" ✓ slide-0_cover.png")

    save(render_slide3(), OUT / "slide-3_proof.png")
    print(" ✓ slide-3_proof.png")

    save(render_slide4(), OUT / "slide-4_diferencia.png")
    print(" ✓ slide-4_diferencia.png")

    save(render_slide5(), OUT / "slide-5_cta.png")
    print(" ✓ slide-5_cta.png")

    # Slide 1 — animated counter sequence
    n = gen_slide1_sequence(OUT / "slide-1_hook")
    print(f" ✓ slide-1_hook/  ({n} frames + final.png)")

    # Slide 2 — 3 stair keyframes for crossfade
    gen_slide2_keyframes(OUT / "slide-2_stairs")
    print(" ✓ slide-2_stairs/  (state-1, state-2, state-3, state-4, final)")

    print("Done.")

if __name__ == "__main__":
    main()
