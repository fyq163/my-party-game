# Integration notes (this repo)

- **Where it lives:** `tools/black_collage/` next to `tools/slice_mahjong.py`. No new top-level concept under `games/`.
- **Show contract:** root `rundown.yaml` lists `game | ppt | video`. A generated deck is a `ppt` row with `path` pointing at the packed `.pptx` (not at these Python scripts).
- **Fonts:** OFL handwriting TTFs stay in `tools/black_collage/fonts/`. Mahjong still uses ignored `assets/private/fonts/` (LXGW WenKai). Do not mix the two.
- **Privacy:** host photos / `cutout_*.png` / preview `.pptx` stay local (gitignored). Decor hearts/stars/arrows in `assets/` are the only images in git.
- **Verify headless:** `python3 tools/black_collage/generate_slides.py` (needs cutouts) — no Tk windows.
