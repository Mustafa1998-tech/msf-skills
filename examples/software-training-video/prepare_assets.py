"""Rebuild the checked-in fictional board PNGs and synthetic audio (optional)."""
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / "assets"
PAPER = "#f6f8fc"
INK = "#182741"
BLUE = "#2755b5"
BORDER = "#dce4f0"
FONT = "DejaVuSans.ttf"
BOLD = "DejaVuSans-Bold.ttf"


def fixture(locale, stage):
    ar = locale == "ar"
    image = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(image)

    def text(x, y, en, arabic, size=33, bold=False, color=INK, anchor=None):
        d.text((x, y), arabic if ar else en, fill=color,
               font=ImageFont.truetype(BOLD if bold else FONT, size),
               direction="rtl" if ar else "ltr", anchor=anchor or ("ra" if ar else "la"))

    def rect(box, fill, outline=None, radius=24):
        d.rounded_rectangle(box, radius, fill, outline, 2 if outline else 1)

    d.rectangle((0, 0, 1920, 109), fill="#142544")
    text(1740 if ar else 180, 26, "WORKBENCH  /  TRAINING", "منصة العمل  /  تدريب",
         36, True, "#f1f5ff")
    rect((1460, 29, 1745, 79) if not ar else (180, 29, 465, 79), "#25406d")
    text(1600 if not ar else 325, 43, "SYNTHETIC DEMO", "مثال اصطناعي",
         24, True, "#f1f5ff", "mt")
    text(1740 if ar else 180, 155, "Sample board", "لوحة تجريبية", 64, True)
    text(1740 if ar else 180, 241, "Track the status of a practice task.",
         "تابع حالة مهمة تدريبية.", 32, color="#485d7a")

    rect((180, 340, 1740, 855 if stage == 1 else 785), "#ffffff", BORDER)
    d.line((220, 458, 1700, 458), fill=BORDER, width=3)
    text(1695 if ar else 225, 376, "TASK", "المهمة", 28, True, "#485d7a")
    text(785 if ar else 1135, 376, "STATUS", "الحالة", 28, True, "#485d7a")
    text(1695 if ar else 225, 513, "Review sample form", "مراجعة نموذج تجريبي",
         43, True)
    text(1695 if ar else 225, 580, "DEMO-001", "DEMO-001", 26, color="#485d7a")

    status = (335, 489, 825, 570) if ar else (1095, 489, 1585, 570)
    rect(status, "#e1f5ea" if stage == 2 else "#e8efff")
    text(580 if ar else 1340, 513, "Ready for review" if stage == 2 else "In progress",
         "جاهزة للمراجعة" if stage == 2 else "قيد التنفيذ", 36, True,
         "#196846" if stage == 2 else BLUE, "mt")
    if stage == 2:
        rect((335, 639, 825, 720) if ar else (1095, 639, 1585, 720), "#dceee4")
        text(580 if ar else 1340, 665, "Change saved", "تم حفظ التغيير", 30, True,
             "#196846", "mt")
    elif stage == 1:
        rect((335, 628, 825, 812) if ar else (1095, 628, 1585, 812), "#f2f5fb", BORDER)
        text(580 if ar else 1340, 649, "In progress", "قيد التنفيذ", 26,
             color="#485d7a", anchor="mt")
        rect((350, 710, 810, 787) if ar else (1110, 710, 1570, 787), BLUE)
        text(580 if ar else 1340, 732, "Ready for review", "جاهزة للمراجعة", 30, True,
             "#ffffff", "mt")
    else:
        rect((335, 639, 825, 720) if ar else (1095, 639, 1585, 720), BLUE)
        text(580 if ar else 1340, 665, "Update status", "تحديث الحالة", 30, True,
             "#ffffff", "mt")
    image.save(ROOT / f"{locale}-{stage + 1}.png", optimize=True)


if __name__ == "__main__":
    ROOT.mkdir(exist_ok=True)
    for language in ("en", "ar"):
        for scene in range(3):
            fixture(language, scene)
    for stem, text in [
        ("en-intro", "Open the sample board and select Update status."),
        ("en-select", "Choose Ready for review from the status list."),
        ("en-confirm", "Verify that the status changed and the board says Change saved."),
    ]:
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                        f"flite=text={text}:voice=slt", "-c:a", "aac",
                        "-b:a", "64k", str(ROOT / f"{stem}.m4a")], check=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                    "sine=frequency=392:duration=1.5:sample_rate=48000",
                    "-af", "afade=t=in:d=0.25,afade=t=out:st=0.7:d=0.8,volume=0.30",
                    "-c:a", "aac", "-b:a", "64k", str(ROOT / "ambient.m4a")], check=True)
