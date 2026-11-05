import os, glob, re
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
MANIFEST = "android/app/src/main/AndroidManifest.xml"
ORANGE = (180, 83, 9)
DARK = (12, 10, 9)

# 1. permissions
m = open(MANIFEST, encoding="utf-8").read()
perms = [
    '<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" android:maxSdkVersion="32" />',
    '<uses-permission android:name="android.permission.USE_EXACT_ALARM" />',
    '<uses-permission android:name="android.permission.VIBRATE" />',
    '<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />',
]
add = "".join("\n    " + p for p in perms if p.split('"')[1] not in m)
m = m.replace("</manifest>", add + "\n</manifest>")
open(MANIFEST, "w", encoding="utf-8").write(m)

# 2. icons
def clock(size, bg=None, radius=0.30):
    im = Image.new("RGBA", (size, size), bg + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size / 2
    r = size * radius
    d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 248, 230), outline=(60, 30, 0), width=max(2, int(size * 0.025)))
    w = max(2, int(size * 0.035))
    d.line([c, c, c, c - r * 0.7], fill=(60, 30, 0), width=w)
    d.line([c, c, c + r * 0.5, c + r * 0.25], fill=(60, 30, 0), width=w)
    d.ellipse([c - w, c - w, c + w, c + w], fill=(60, 30, 0))
    return im

legacy = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for dens, px in legacy.items():
    folder = f"{RES}/mipmap-{dens}"
    clock(px, ORANGE).save(f"{folder}/ic_launcher.png")
    sq = clock(px, ORANGE)
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, px - 1, px - 1], fill=255)
    rnd = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    rnd.paste(sq, (0, 0), mask)
    rnd.save(f"{folder}/ic_launcher_round.png")
    fg = int(px * 108 / 48)
    clock(fg, None, 0.27).save(f"{folder}/ic_launcher_foreground.png")

open(f"{RES}/values/ic_launcher_background.xml", "w").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#B45309</color>\n</resources>\n')

# 3. splash screens: dark background with the clock
for p in glob.glob(f"{RES}/drawable*/splash.png"):
    w, h = Image.open(p).size
    im = Image.new("RGB", (w, h), DARK)
    s = int(min(w, h) * 0.4)
    ic = clock(s, ORANGE)
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=255)
    im.paste(ic.convert("RGB"), ((w - s) // 2, (h - s) // 2), mask)
    im.save(p)

# 4. dark status bar and background colors
colors = f"{RES}/values/colors.xml"
open(colors, "w").write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="colorPrimary">#0C0A09</color>\n    <color name="colorPrimaryDark">#0C0A09</color>\n    <color name="colorAccent">#F59E0B</color>\n</resources>\n')
print("prepared")
