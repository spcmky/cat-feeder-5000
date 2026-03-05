#!/usr/bin/env python3
"""Add part labels with leader lines to assembly renders."""

from PIL import Image, ImageDraw, ImageFont
import sys

# Try to get a clean font, fall back to default
try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    FONT_BOLD = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
except:
    FONT = ImageFont.load_default()
    FONT_BOLD = FONT

BG_COLOR = (255, 255, 255, 200)
TEXT_COLOR = (30, 30, 30)
LINE_COLOR = (60, 60, 60)
DOT_COLOR = (255, 50, 50)
DOT_R = 4


def add_label(draw, text, label_xy, target_xy, align="left"):
    """Draw a label with a leader line to a target point."""
    lx, ly = label_xy
    tx, ty = target_xy

    # Draw leader line
    draw.line([lx, ly, tx, ty], fill=LINE_COLOR, width=1)

    # Draw target dot
    draw.ellipse([tx-DOT_R, ty-DOT_R, tx+DOT_R, ty+DOT_R], fill=DOT_COLOR)

    # Measure text
    bbox = draw.textbbox((0, 0), text, font=FONT)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 4

    # Position label box
    if align == "right":
        bx = lx - tw - 2*pad
    else:
        bx = lx
    by = ly - th//2 - pad

    # Draw background
    draw.rectangle([bx-pad, by, bx+tw+pad, by+th+2*pad], fill=BG_COLOR, outline=LINE_COLOR)

    # Draw text
    draw.text((bx, by+pad), text, fill=TEXT_COLOR, font=FONT)


def label_corner():
    """Label the corner/isometric view."""
    img = Image.open("3d-models/renders/assembly_corner.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)

    # Part labels: (text, label_position, target_point, alignment)
    labels = [
        # Top area
        ("1. Hopper Lid",          (50, 40),    (640, 95),    "left"),
        ("2. Hopper",              (50, 80),    (600, 260),   "left"),
        ("3. Auger Tube+Screw",    (50, 120),   (550, 430),   "left"),
        ("4. Motor Mount",         (1200, 40),  (1000, 280),  "right"),
        ("5. Camera Mount",        (1200, 80),  (1040, 340),  "right"),

        # Mid area
        ("6. Gate Servo Bracket",  (1200, 160), (880, 470),   "right"),
        ("7. Gate Bumper (TPU)",   (1200, 200), (850, 490),   "right"),
        ("8. Gate Hinge Mount",    (1200, 240), (820, 430),   "right"),
        ("9. Gate Flap",           (1200, 320), (870, 570),   "right"),

        # Lower area
        ("10. RFID Halo Arch",     (1200, 440), (1020, 670),  "right"),
        ("11. Bowl",               (50, 560),   (500, 650),   "left"),
        ("12. Bowl Shelf",         (50, 600),   (580, 780),   "left"),
        ("13. Electronics Tray",   (50, 340),   (350, 550),   "left"),
        ("14. Rear Box (Body)",    (50, 260),   (420, 500),   "left"),

        # Bottom
        ("15. Halo Feet",          (1200, 560), (1060, 870),  "right"),
        ("16. TPU Feet",           (50, 860),   (250, 900),   "left"),
    ]

    for text, label_xy, target_xy, align in labels:
        add_label(draw, text, label_xy, target_xy, align)

    # Title
    draw.text((20, 1160), "Cat Feeder 5000 — Corner View (Labeled)", fill=TEXT_COLOR, font=FONT_BOLD)

    result = Image.alpha_composite(img, overlay)
    result = result.convert("RGB")
    result.save("3d-models/renders/assembly_corner_labeled.png")
    print("Saved: assembly_corner_labeled.png")


def label_front():
    """Label the front view."""
    img = Image.open("3d-models/renders/assembly_front.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)

    labels = [
        ("1. Hopper",             (50, 40),    (680, 120),   "left"),
        ("2. Camera Mount",       (1200, 40),  (1150, 250),  "right"),
        ("3. Gate Servo Bracket", (1200, 120), (900, 370),   "right"),
        ("4. Gate Bumper (TPU)",  (1200, 170), (830, 420),   "right"),
        ("5. Auger Screw",       (50, 200),   (700, 450),   "left"),
        ("6. RFID Halo Arch",    (50, 500),   (550, 620),   "left"),
        ("7. Gate Flap",         (1200, 350), (830, 550),   "right"),
        ("8. Rear Box (Body)",   (1200, 250), (1020, 350),  "right"),
    ]

    for text, label_xy, target_xy, align in labels:
        add_label(draw, text, label_xy, target_xy, align)

    draw.text((20, 1160), "Cat Feeder 5000 — Front View (Labeled)", fill=TEXT_COLOR, font=FONT_BOLD)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save("3d-models/renders/assembly_front_labeled.png")
    print("Saved: assembly_front_labeled.png")


def label_side():
    """Label the side view."""
    img = Image.open("3d-models/renders/assembly_side.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)

    labels = [
        ("1. Hopper + Lid",       (50, 40),    (700, 120),   "left"),
        ("2. Camera Mount",       (50, 120),   (280, 310),   "left"),
        ("3. Gate Servo Bracket", (50, 240),   (380, 450),   "left"),
        ("4. Auger Tube",         (1200, 80),  (920, 350),   "right"),
        ("5. Rear Box (Body)",    (1200, 200), (1000, 500),  "right"),
        ("6. RFID Halo Arch",     (50, 400),   (220, 550),   "left"),
        ("7. Gate Flap",          (50, 500),   (370, 580),   "left"),
        ("8. Bowl",               (50, 600),   (350, 720),   "left"),
        ("9. Bowl Shelf",         (50, 700),   (400, 790),   "left"),
        ("10. Floor Plate",       (1200, 600), (900, 830),   "right"),
        ("11. TPU Feet",          (1200, 700), (1100, 870),  "right"),
        ("12. Halo Foot",         (50, 820),   (140, 880),   "left"),
    ]

    for text, label_xy, target_xy, align in labels:
        add_label(draw, text, label_xy, target_xy, align)

    draw.text((20, 1160), "Cat Feeder 5000 — Side View (Labeled)", fill=TEXT_COLOR, font=FONT_BOLD)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save("3d-models/renders/assembly_side_labeled.png")
    print("Saved: assembly_side_labeled.png")


if __name__ == "__main__":
    label_corner()
    label_front()
    label_side()
    print("Done!")
