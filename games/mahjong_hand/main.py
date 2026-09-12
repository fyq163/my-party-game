"""Mahjong hand display: show 11/12 tiles, no interaction."""
import argparse
import json
import random
from pathlib import Path

from PIL import Image

W, H, GAP, PAD = 120, 168, 8, 24
BASE = Path(__file__).resolve().parents[2] / "assets" / "mahjong"
SUIT_ORDER = {"tong": 0, "tiao": 1, "wan": 2, "wind": 3, "dragon": 4}


def load_ids() -> tuple[list[str], dict[str, Path]]:
    data = json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))
    return [d["id"] for d in data], {d["id"]: BASE / d["file"] for d in data}


def sort_key(tid: str) -> tuple[int, str]:
    suit, _, rank = tid.partition("_")
    return (SUIT_ORDER.get(suit, 9), rank)


def resolve_hand(ids: list[str], hand: str | None, count: int, seed: int | None) -> list[str]:
    if hand:
        tiles = [t.strip() for t in hand.split(",") if t.strip()]
        bad = [t for t in tiles if t not in set(ids)]
        if bad:
            raise SystemExit(f"invalid tile id: {', '.join(bad)}")
        return sorted(tiles, key=sort_key)
    rng = random.Random(seed)
    return sorted(rng.choices(ids, k=count), key=sort_key)


def title_text(hand: list[str]) -> str:
    groups: dict[str, list[str]] = {}
    for tid in hand:
        suit, _, rank = tid.partition("_")
        name = suit.capitalize()
        label = rank.capitalize() if suit == "wind" else rank
        groups.setdefault(name, []).append(label)
    return " | ".join(f"{k}: {' '.join(v)}" for k, v in sorted(groups.items()))


def compose(hand: list[str], files: dict[str, Path]) -> Image.Image:
    img = Image.new("RGB", (PAD * 2 + W * len(hand) + GAP * (len(hand) - 1), PAD * 2 + H), "white")
    for i, tid in enumerate(hand):
        tile = Image.open(files[tid]).convert("RGBA")
        if tile.size != (W, H):
            tile = tile.resize((W, H))
        img.paste(tile, (PAD + i * (W + GAP), PAD), tile)
    return img


def show(hand: list[str], files: dict[str, Path]) -> None:
    import tkinter as tk

    from PIL import ImageTk

    img = compose(hand, files)
    root = tk.Tk()
    root.title(title_text(hand))
    photo = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(root, width=img.width, height=img.height + 24, bg="white", highlightthickness=0)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.create_text(img.width // 2, img.height + 12, text="python main.py --hand wan_1,wan_2,wan_3 --count 12 --save hand.png",
                      font=("TkDefaultFont", 10), fill="gray")
    root.mainloop()  # ponytail: keep ref via Tk image registry, no extra var needed


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Show a mahjong hand (display only).")
    p.add_argument("--count", type=int, choices=[11, 12], default=11)
    p.add_argument("--hand", type=str, default=None, help="comma-separated tile ids")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--save", type=str, default=None, help="save stitched image, skip window")
    args = p.parse_args(argv)
    ids, files = load_ids()
    hand = resolve_hand(ids, args.hand, args.count, args.seed)
    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        compose(hand, files).save(out)
        print(f"saved {len(hand)} tiles -> {out}")
        return
    show(hand, files)


if __name__ == "__main__":
    main()
