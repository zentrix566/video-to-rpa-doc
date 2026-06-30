# -*- coding: utf-8 -*-
"""
Create a demo screen-recording style video with scene changes for testing.
Simulates an RPA workflow: Login -> Fill Form -> Submit -> Success.
"""
import cv2
import datetime
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

# Settings
WIDTH, HEIGHT = 1280, 720
FPS = 30

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, f"demo_screen_recording_{_timestamp}.mp4")

# Scene durations (seconds)
SCENES = [
    ("桌面 - 双击打开系统", 3),
    ("登录页面 - 输入账号密码", 4),
    ("数据录入页面 - 填写表单", 5),
    ("提交确认弹窗 - 点击确定", 3),
    ("成功提示 - 操作完成", 3),
    ("返回桌面 - 流程结束", 2),
]


def _load_font(size):
    """Try loading a system font that supports Chinese."""
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyhbd.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def cv2_puttext_chinese(img, text, pos, font_size=24, color=(255, 255, 255)):
    """Draw Chinese text on an OpenCV image (BGR) using Pillow."""
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = _load_font(font_size)
    draw.text(pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def cv2_puttext_centered(img, text, center_y, font_size=24, color=(255, 255, 255)):
    """Draw centered Chinese text horizontally."""
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = _load_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) // 2
    draw.text((x, center_y), text, font=font, fill=color)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def draw_scene(name, width=WIDTH, height=HEIGHT):
    """Draw a fake UI screen based on scene name."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    if "桌面" in name:
        img[:, :] = (30, 120, 180)
        img = cv2_puttext_chinese(img, "Windows Desktop", (50, 30), font_size=36, color=(255, 255, 255))
        cv2.rectangle(img, (200, 150), (500, 400), (200, 200, 200), -1)
        img = cv2_puttext_centered(img, "ERP System", 260, font_size=28, color=(0, 0, 0))
    elif "登录" in name:
        img[:, :] = (240, 240, 240)
        cv2.rectangle(img, (340, 100), (940, 620), (255, 255, 255), -1)
        img = cv2_puttext_centered(img, "Login", 150, font_size=48, color=(50, 50, 50))
        cv2.rectangle(img, (400, 280), (880, 340), (230, 230, 230), -1)
        img = cv2_puttext_chinese(img, "Username", (420, 290), font_size=22, color=(80, 80, 80))
        cv2.rectangle(img, (400, 400), (880, 460), (230, 230, 230), -1)
        img = cv2_puttext_chinese(img, "Password", (420, 410), font_size=22, color=(80, 80, 80))
        cv2.rectangle(img, (520, 520), (760, 580), (0, 120, 255), -1)
        img = cv2_puttext_centered(img, "Login", 535, font_size=28, color=(255, 255, 255))
    elif "数据录入" in name or "表单" in name:
        img[:, :] = (245, 245, 245)
        cv2.rectangle(img, (0, 0), (width, 60), (0, 100, 200), -1)
        img = cv2_puttext_chinese(img, "Data Entry - Order Form", (30, 12), font_size=26, color=(255, 255, 255))
        fields = [
            ("Order No:   20250629-001", 120),
            ("Customer:   ABC Company", 200),
            ("Product:    Widget-X200", 280),
            ("Quantity:   500", 360),
            ("Price:      $12.50", 440),
        ]
        for text, y in fields:
            cv2.rectangle(img, (80, y), (600, y + 50), (255, 255, 255), -1)
            img = cv2_puttext_chinese(img, text, (100, y + 8), font_size=20, color=(50, 50, 50))
        cv2.rectangle(img, (700, 520), (1000, 580), (0, 150, 0), -1)
        img = cv2_puttext_centered(img, "Submit", 535, font_size=32, color=(255, 255, 255))
    elif "提交确认" in name or "弹窗" in name:
        img[:, :] = (245, 245, 245)
        overlay = np.full((height, width, 3), (100, 100, 100), dtype=np.uint8)
        img = cv2.addWeighted(img, 0.3, overlay, 0.7, 0)
        cv2.rectangle(img, (340, 200), (940, 500), (255, 255, 255), -1)
        img = cv2_puttext_centered(img, "Confirm Submit?", 250, font_size=36, color=(50, 50, 50))
        img = cv2_puttext_centered(img, "Are you sure to submit this order?", 320, font_size=22, color=(80, 80, 80))
        cv2.rectangle(img, (420, 400), (640, 460), (0, 150, 0), -1)
        img = cv2_puttext_centered(img, "OK", 415, font_size=26, color=(255, 255, 255))
        cv2.rectangle(img, (680, 400), (900, 460), (200, 200, 200), -1)
        img = cv2_puttext_centered(img, "Cancel", 415, font_size=26, color=(50, 50, 50))
    elif "成功" in name:
        img[:, :] = (240, 248, 255)
        center = (width // 2, 300)
        cv2.circle(img, center, 80, (0, 200, 0), -1)
        img = cv2_puttext_centered(img, "V", 275, font_size=48, color=(255, 255, 255))
        img = cv2_puttext_centered(img, "Submit Successful!", 420, font_size=32, color=(0, 150, 0))
        img = cv2_puttext_centered(img, "Order No: 20250629-001 has been saved.", 490, font_size=20, color=(80, 80, 80))
    else:
        img[:, :] = (30, 120, 180)
        img = cv2_puttext_chinese(img, "Done", (50, 30), font_size=36, color=(255, 255, 255))

    # Add scene label at bottom
    cv2.rectangle(img, (0, height - 50), (width, height), (0, 0, 0), -1)
    img = cv2_puttext_chinese(img, name, (20, height - 42), font_size=20, color=(255, 255, 255))
    return img


def create_video(output_path, scenes, fps=FPS):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (WIDTH, HEIGHT))
    if not out.isOpened():
        print(f"ERROR: Cannot open VideoWriter for {output_path}")
        return

    for name, duration in scenes:
        frame = draw_scene(name)
        frames = int(duration * fps)
        for _ in range(frames):
            out.write(frame)
        print(f"Scene: {name} ({duration}s, {frames} frames)")

    out.release()
    print(f"\nDemo video saved: {output_path}")


if __name__ == '__main__':
    create_video(OUTPUT_PATH, SCENES)
