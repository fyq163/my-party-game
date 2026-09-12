"""Slice mahjong source.jpg (5x9 grid) into 32 tiles, or draw placeholders."""
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("缺少 Pillow，请先安装：pip install Pillow")
    sys.exit(1)

W, H, R = 120, 168, 14
INSET = 0.045
BASE = Path(__file__).resolve().parent.parent / "assets" / "mahjong"
SRC = BASE / "source.jpg"
OUT = BASE / "tiles"

CN = "一二三四五六七八九"
WINDS = [("east", "東"), ("south", "南"), ("west", "西"), ("north", "北")]

# (id, row, col, suit, rank, label)
TILES = (
    [(f"tong_{i}", 0, i - 1, "tong", i, f"{CN[i-1]}筒") for i in range(1, 10)]
    + [(f"tiao_{i}", 1, i - 1, "tiao", i, f"{CN[i-1]}條") for i in range(1, 10)]
    + [(f"wan_{i}", 2, i - 1, "wan", i, f"{CN[i-1]}萬") for i in range(1, 10)]
    + [(f"wind_{n}", 3, c, "wind", n, ch) for c, (n, ch) in enumerate(WINDS)]
    + [("dragon_red", 3, 4, "dragon", "red", "中")]
)

# pip layouts on 3x3 grid (indices 0..8)
LAYOUT = {1: [4], 2: [1, 7], 3: [1, 4, 7], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8],
          6: [0, 2, 3, 5, 6, 8], 7: [0, 2, 3, 4, 5, 6, 8],
          8: [0, 1, 2, 3, 5, 6, 7, 8], 9: list(range(9))}
XS = [30, 60, 90]
YS = [44, 84, 124]


def _font(n):
    # ponytail: 楷体放本机私有目录（不入库，各生成机自备），没有时回退系统黑体
    for p in (str(Path(__file__).resolve().parent.parent / "assets" / "private" / "fonts" / "LXGWWenKai-Medium.ttf"),
              "/System/Library/Fonts/Hiragino Sans GB.ttc",
              "/System/Library/Fonts/PingFang.ttc",
              "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
              "C:/Windows/Fonts/msyh.ttc"):
        try:
            return ImageFont.truetype(p, n)
        except Exception:
            pass
    return ImageFont.load_default()


def _mask():
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, H - 1], R, fill=255)
    return m


def _border(img):
    ImageDraw.Draw(img).rounded_rectangle([1, 1, W - 2, H - 2], R, outline=(180, 180, 180), width=2)


def _base():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, W - 1, H - 1], R, fill=(255, 255, 255, 255))
    return img


def _tong(d, rank):
    r = 26 if rank == 1 else 11
    # ponytail: 7筒3上4下——上3斜置红筒，下4蓝筒 2×2（7筒上下反转）
    if rank == 7:
        # 上3个斜着，红色
        for x, y in [(30, 24), (60, 42), (90, 60)]:
            c, f = (200, 40, 40), (255, 220, 220)
            d.ellipse([x - r, y - r, x + r, y + r], fill=f, outline=c, width=3)
            d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], outline=c, width=2)
        # 下4个 2×2，蓝色
        for x, y in [(34, 100), (86, 100), (34, 130), (86, 130)]:
            c, f = (30, 100, 200), (220, 235, 255)
            d.ellipse([x - r, y - r, x + r, y + r], fill=f, outline=c, width=3)
            d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], outline=c, width=2)
        return
    # ponytail: 8筒2列×4行，全蓝
    if rank == 8:
        for x, y in [(40, 36), (80, 36), (40, 68), (80, 68),
                     (40, 100), (80, 100), (40, 132), (80, 132)]:
            c, f = (30, 100, 200), (220, 235, 255)
            d.ellipse([x - r, y - r, x + r, y + r], fill=f, outline=c, width=3)
            d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], outline=c, width=2)
        return
    for idx in LAYOUT[rank]:
        x, y = XS[idx % 3], YS[idx // 3]
        red = rank % 2 == 1 and idx == 4
        c, f = ((200, 40, 40), (255, 220, 220)) if red else ((30, 100, 200), (220, 235, 255))
        d.ellipse([x - r, y - r, x + r, y + r], fill=f, outline=c, width=3)
        d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], outline=c, width=2)


def _tiao(d, rank):
    # ponytail: 8条特殊布局——上4倒M、下4正M，上下对称
    if rank == 8:
        pts = [(30, 38), (50, 52), (70, 52), (90, 38),
               (30, 130), (50, 116), (70, 116), (90, 130)]
        for x, y in pts:
            bw, bh = 12, 26
            c, f = (20, 120, 40), (60, 180, 80)
            d.rounded_rectangle([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 4, fill=f, outline=c, width=2)
            d.line([x, y - bh / 2 + 3, x, y + bh / 2 - 3], fill=c, width=2)
        return
    for idx in LAYOUT[rank]:
        x, y = XS[idx % 3], YS[idx // 3]
        if rank == 1:
            x, y, bw, bh = 60, 84, 20, 76
        else:
            bw, bh = 12, 26
        red = rank % 2 == 1 and idx == 4
        c, f = ((200, 40, 40), (255, 200, 200)) if red else ((20, 120, 40), (60, 180, 80))
        d.rounded_rectangle([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 4, fill=f, outline=c, width=2)
        d.line([x, y - bh / 2 + 3, x, y + bh / 2 - 3], fill=c, width=2)


def _text_center(d, y, s, size, fill):
    f = _font(size)
    bb = d.textbbox((0, 0), s, font=f)
    # ponytail: stroke 充粗体，毛笔字本身细时也显粗
    d.text((W / 2 - (bb[2] - bb[0]) / 2 - bb[0], y), s, font=f, fill=fill,
           stroke_width=max(1, size // 32), stroke_fill=fill)


def placeholder(tid, suit, rank, label):
    img = _base()
    d = ImageDraw.Draw(img)
    if suit == "tong":
        _tong(d, rank)
    elif suit == "tiao":
        _tiao(d, rank)
    elif suit == "wan":
        _text_center(d, 28, CN[rank - 1], 52, (30, 30, 30))
        _text_center(d, 88, "萬", 44, (200, 40, 40))
    elif suit == "dragon":
        _text_center(d, 42, label, 64, (200, 40, 40))
    else:
        _text_center(d, 42, label, 64, (30, 30, 30))
    _border(img)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    src = None
    if SRC.exists():
        src = Image.open(SRC).convert("RGB")
        print(f"使用源图: {SRC} ({src.width}x{src.height})")
    else:
        print(f"提示: 未找到 {SRC}，将程序化生成占位牌面（放一张 source.jpg 即可切真实牌面）。")
    mask = _mask()
    for tid, row, col, suit, rank, label in TILES:
        if src is not None:
            sw, sh = src.width / 9, src.height / 5
            box = (int((col + INSET) * sw), int((row + INSET) * sh),
                   int((col + 1 - INSET) * sw), int((row + 1 - INSET) * sh))
            img = src.crop(box).resize((W, H), Image.LANCZOS).convert("RGBA")
            img.putalpha(mask)
            _border(img)
        else:
            img = placeholder(tid, suit, rank, label)
        img.save(OUT / f"{tid}.png")
    manifest = [{"id": t, "file": f"tiles/{t}.png", "suit": s, "rank": r, "label": lb}
                for t, _, _, s, r, lb in TILES]
    (BASE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE / "README.md").write_text(
        "# 麻将牌面\n\n来源：`assets/mahjong/source.jpg`（5行×9列全图，用户上传）。"
        "无源图时脚本程序化生成占位牌面。\n\n- 输出：`tiles/` 下 32 张 PNG（tong/tiao/wan 各 1..9 + wind east/south/west/north + dragon_red 红中）\n"
        "- 尺寸：统一 120×168，透明圆角（R≈14），白底 + 细灰描边\n"
        "- 切片：单格 W/9 × H/5，内缩 inset 0.045 去黑缝，再 resize + 圆角蒙版\n"
        "- 运行：`python3 tools/slice_mahjong.py`\n", encoding="utf-8")
    ok = sum(1 for t, *_ in TILES if (OUT / f"{t}.png").exists())
    print(f"已生成 {ok}/{len(TILES)} 张 → {OUT}，manifest {len(manifest)} 条")


if __name__ == "__main__":
    main()
