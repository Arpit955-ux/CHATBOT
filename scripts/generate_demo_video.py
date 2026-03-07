from __future__ import annotations

import math
from pathlib import Path
from typing import List

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "demo"
OUT_PATH = OUT_DIR / "quotes-chatbot-demo.mp4"

WIDTH = 1280
HEIGHT = 720
FPS = 24


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
            ]
        )
    candidates.extend(
        [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        ]
    )
    for c in candidates:
        p = Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font(64, bold=True)
FONT_SUBTITLE = load_font(36)
FONT_BODY = load_font(30)
FONT_CODE = load_font(28)
FONT_CHAT = load_font(28)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def ease_out(t: float) -> float:
    return 1 - (1 - t) ** 3


def gradient_bg() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), "#1b2c5f")
    px = img.load()
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(lerp(36, 102, t))
        g = int(lerp(58, 92, t))
        b = int(lerp(108, 189, t))
        for x in range(WIDTH):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse((50, 40, 380, 370), fill=(255, 255, 255, 45))
    draw.ellipse((920, 460, 1250, 790), fill=(255, 255, 255, 50))
    return img


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, font: ImageFont.ImageFont, fill: str) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    draw.text((x, y), text, font=font, fill=fill)


def scene_title(frames: int) -> List[Image.Image]:
    out: List[Image.Image] = []
    for i in range(frames):
        t = ease_out(i / max(frames - 1, 1))
        img = gradient_bg()
        draw = ImageDraw.Draw(img, "RGBA")

        card_w = int(950 * (0.9 + 0.1 * t))
        card_h = int(420 * (0.9 + 0.1 * t))
        x0 = (WIDTH - card_w) // 2
        y0 = (HEIGHT - card_h) // 2
        draw.rounded_rectangle((x0, y0, x0 + card_w, y0 + card_h), radius=30, fill=(255, 255, 255, 60), outline=(255, 255, 255, 120), width=2)

        draw_centered(draw, "Quotes Recommendation Chatbot", y0 + 90, FONT_TITLE, "white")
        draw_centered(draw, "Rasa NLP + Flask Web Interface", y0 + 200, FONT_SUBTITLE, "#f2f6ff")
        draw_centered(draw, "Live Demo", y0 + 270, FONT_SUBTITLE, "#f9f2ff")

        out.append(img)
    return out


def scene_run_steps(frames: int) -> List[Image.Image]:
    out: List[Image.Image] = []
    steps = [
        "git clone https://github.com/Arpit955-ux/CHATBOT.git",
        "cd CHATBOT",
        "./run.sh",
        "Open URL shown in terminal (example: http://127.0.0.1:5001)",
    ]
    for i in range(frames):
        img = gradient_bg()
        draw = ImageDraw.Draw(img, "RGBA")
        draw.rounded_rectangle((120, 100, 1160, 620), radius=28, fill=(16, 26, 54, 165), outline=(220, 230, 255, 130), width=2)
        draw.text((180, 150), "How To Run", font=FONT_TITLE, fill="white")

        visible = min(len(steps), 1 + int((i / max(frames - 1, 1)) * len(steps) * 1.1))
        y = 250
        for idx, step in enumerate(steps[:visible], start=1):
            draw.text((180, y), f"{idx}. {step}", font=FONT_CODE, fill="#e8f0ff")
            y += 78

        out.append(img)
    return out


def chat_bubble(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, user: bool = False) -> int:
    max_w = 780
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), candidate, font=FONT_CHAT)
        if bbox[2] - bbox[0] <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    line_h = 36
    h = 26 + len(lines) * line_h
    w = 0
    for line in lines:
        lw = draw.textbbox((0, 0), line, font=FONT_CHAT)[2]
        w = max(w, lw)
    w += 36

    if user:
        x = WIDTH - 140 - w
        fill = (34, 114, 255, 255)
        text_color = "white"
    else:
        fill = (228, 232, 240, 255)
        text_color = "#1c2230"

    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=fill)
    ty = y + 12
    for line in lines:
        draw.text((x + 18, ty), line, font=FONT_CHAT, fill=text_color)
        ty += line_h

    return h + 18


def scene_chat_demo(frames: int) -> List[Image.Image]:
    out: List[Image.Image] = []
    timeline = [
        ("bot", "Hey hi, please tell me which quotes you want today (Inspirational/Motivational/Success/Love/Funny)."),
        ("user", "inspirational quote"),
        ("bot", "Here's an inspirational quote for you:"),
        ("bot", "Believe you can, and you're halfway there. - Theodore Roosevelt"),
        ("bot", "Is this quote helpful to you? Type 'yes' or 'no'."),
        ("user", "yes"),
        ("bot", "Thanks for your feedback. If you want more quotes, mention the quote type."),
    ]

    for i in range(frames):
        img = gradient_bg()
        draw = ImageDraw.Draw(img, "RGBA")

        draw.rounded_rectangle((180, 56, 1100, 664), radius=18, fill=(245, 247, 251, 255), outline=(210, 216, 228, 255), width=2)
        draw.rectangle((180, 56, 1100, 130), fill=(255, 255, 255, 255))
        draw.text((520, 80), "Quotes Bot", font=FONT_SUBTITLE, fill="#232a3a")

        # Grow number of shown messages over time.
        shown = min(len(timeline), 1 + int((i / max(frames - 1, 1)) * (len(timeline) + 1)))
        y = 160
        for role, text in timeline[:shown]:
            y += chat_bubble(draw, x=220, y=y, text=text, user=(role == "user"))
            if y > 590:
                break

        out.append(img)
    return out


def scene_outro(frames: int) -> List[Image.Image]:
    out: List[Image.Image] = []
    for i in range(frames):
        t = ease_out(i / max(frames - 1, 1))
        img = gradient_bg()
        draw = ImageDraw.Draw(img, "RGBA")
        alpha = int(130 + 100 * t)
        draw.rounded_rectangle((120, 170, 1160, 550), radius=30, fill=(20, 30, 58, alpha), outline=(255, 255, 255, 150), width=2)

        draw_centered(draw, "Demo Complete", 240, FONT_TITLE, "white")
        draw_centered(draw, "Repository", 340, FONT_SUBTITLE, "#dce7ff")
        draw_centered(draw, "github.com/Arpit955-ux/CHATBOT", 390, FONT_BODY, "#ffffff")
        out.append(img)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    frames: List[Image.Image] = []
    frames.extend(scene_title(frames=2 * FPS))
    frames.extend(scene_run_steps(frames=3 * FPS))
    frames.extend(scene_chat_demo(frames=5 * FPS))
    frames.extend(scene_outro(frames=2 * FPS))

    writer = imageio.get_writer(str(OUT_PATH), fps=FPS, codec="libx264", quality=8)
    try:
        for frame in frames:
            writer.append_data(np.asarray(frame))
    finally:
        writer.close()

    print(f"Created demo video: {OUT_PATH}")


if __name__ == "__main__":
    main()
