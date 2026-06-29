# -*- coding: utf-8 -*-
"""
Create a demo screen-recording style video with scene changes for testing.
Simulates an RPA workflow: Login -> Fill Form -> Submit -> Success.
"""
import cv2
import numpy as np
import os

# Settings
WIDTH, HEIGHT = 1280, 720
FPS = 30
OUTPUT_PATH = "demo_screen_recording.mp4"

# Scene durations (seconds)
SCENES = [
    ("桌面 - 双击打开系统", 3),
    ("登录页面 - 输入账号密码", 4),
    ("数据录入页面 - 填写表单", 5),
    ("提交确认弹窗 - 点击确定", 3),
    ("成功提示 - 操作完成", 3),
    ("返回桌面 - 流程结束", 2),
]


def draw_scene(name, width=WIDTH, height=HEIGHT):
    """Draw a fake UI screen based on scene name."""
    # Background
    if "桌面" in name:
        img = np.full((height, width, 3), (30, 120, 180), dtype=np.uint8)
        cv2.putText(img, "Windows Desktop", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        cv2.rectangle(img, (200, 150), (500, 400), (200, 200, 200), -1)
        cv2.putText(img, "ERP System", (260, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    elif "登录" in name:
        img = np.full((height, width, 3), (240, 240, 240), dtype=np.uint8)
        cv2.rectangle(img, (340, 100), (940, 620), (255, 255, 255), -1)
        cv2.putText(img, "Login", (560, 180), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 50, 50), 3)
        cv2.rectangle(img, (400, 280), (880, 340), (230, 230, 230), -1)
        cv2.putText(img, "Username", (420, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 2)
        cv2.rectangle(img, (400, 400), (880, 460), (230, 230, 230), -1)
        cv2.putText(img, "Password", (420, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 2)
        cv2.rectangle(img, (520, 520), (760, 580), (0, 120, 255), -1)
        cv2.putText(img, "Login", (590, 565), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    elif "数据录入" in name or "表单" in name:
        img = np.full((height, width, 3), (245, 245, 245), dtype=np.uint8)
        # Header
        cv2.rectangle(img, (0, 0), (width, 60), (0, 100, 200), -1)
        cv2.putText(img, "Data Entry - Order Form", (30, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        # Form fields
        fields = [("Order No:   20250629-001", 120), ("Customer:   ABC Company", 200),
                  ("Product:    Widget-X200", 280), ("Quantity:   500", 360),
                  ("Price:      $12.50", 440)]
        for text, y in fields:
            cv2.rectangle(img, (80, y), (600, y + 50), (255, 255, 255), -1)
            cv2.putText(img, text, (100, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)
        cv2.rectangle(img, (700, 520), (1000, 580), (0, 150, 0), -1)
        cv2.putText(img, "Submit", (780, 565), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    elif "提交确认" in name or "弹窗" in name:
        # Same background as form but darker overlay
        img = np.full((height, width, 3), (245, 245, 245), dtype=np.uint8)
        overlay = np.full((height, width, 3), (0, 0, 0), dtype=np.uint8)
        overlay[:] = (100, 100, 100)
        img = cv2.addWeighted(img, 0.3, overlay, 0.7, 0)
        # Dialog box
        cv2.rectangle(img, (340, 200), (940, 500), (255, 255, 255), -1)
        cv2.putText(img, "Confirm Submit?", (460, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (50, 50, 50), 3)
        cv2.putText(img, "Are you sure to submit this order?", (380, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (80, 80, 80), 2)
        cv2.rectangle(img, (420, 400), (640, 460), (0, 150, 0), -1)
        cv2.putText(img, "OK", (510, 445), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(img, (680, 400), (900, 460), (200, 200, 200), -1)
        cv2.putText(img, "Cancel", (740, 445), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
    elif "成功" in name:
        img = np.full((height, width, 3), (240, 248, 255), dtype=np.uint8)
        # Green check circle
        center = (width // 2, 300)
        cv2.circle(img, center, 80, (0, 200, 0), -1)
        cv2.putText(img, "V", (width // 2 - 30, 330), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
        cv2.putText(img, "Submit Successful!", (420, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 150, 0), 3)
        cv2.putText(img, "Order No: 20250629-001 has been saved.", (340, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (80, 80, 80), 2)
    else:
        img = np.full((height, width, 3), (30, 120, 180), dtype=np.uint8)
        cv2.putText(img, "Done", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    # Add scene label at bottom
    cv2.rectangle(img, (0, height - 50), (width, height), (0, 0, 0), -1)
    cv2.putText(img, name, (20, height - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
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
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_video(OUTPUT_PATH, SCENES)
