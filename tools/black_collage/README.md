# Black collage PPT toolkit

Party-host tool for **16:9 black scrapbook slides**: photo cutout stickers, pink marker outlines, dotted arrows, and Chinese brush titles.

This lives under `tools/` (same area as `slice_mahjong.py`). It is a **headless Python pipeline**, not a Tauri GUI. Generated `.pptx` files are show assets: pack them into the portable binary and reference them from root `rundown.yaml` as `kind: ppt`.

Handwriting fonts used by the pipeline are **committed here** (`fonts/*.ttf`, SIL OFL). Do **not** put them in `assets/private/fonts/` — that directory is gitignored for mahjong tile generation (LXGW WenKai, etc.).

## Layout

```
tools/black_collage/
  generate_slides.py       # cutouts → sticker PNGs + flattened 16:9 PNG slides + preview.pptx
  generate_jitter.py       # wobble GIFs + layered teeter PPTX (optional motion)
  build_editable_pptx.py   # movable pictures + native text boxes (tweak in Keynote/PPT)
  fonts/                   # Zhi Mang Xing, Ma Shan Zheng, Liu Jian Mao Cao (OFL)
  assets/
    decor_star.png         # pink star (repo)
    decor_heart.png        # pink heart (repo)
    arrow_dotted.png       # dotted arrow (repo)
    cutout_*.png           # YOUR stickers — not committed
```

Do **not** commit personal photo cutouts, birthday/BBQ previews, or sample `.pptx` that embed private images. Generated files are gitignored (see `.gitignore` in this folder).

## Dependencies

Python 3.10+ with:

```bash
python3 -m pip install -r tools/black_collage/requirements.txt
```

(`opencv-python-headless` is enough; no Tk / GUI windows.)

## Host cutouts

Place transparent PNGs in `assets/`:

| file | used on |
| --- | --- |
| `cutout_child.png` | slide 1 |
| `cutout_cake.png` | slide 2 |
| `cutout_artist.png` | slide 2 |
| `cutout_dress.png` | slides 2–3 |
| `cutout_chili.png` | slide 3 |

Optional re-extract from source photos (writes the same `cutout_*.png` names):

```bash
python3 tools/black_collage/generate_slides.py \
  --child /path/to/child_on_black.jpg \
  --collage /path/to/white_bg_collage.jpg
```

`CHILD_IMG` / `COLLAGE_IMG` env vars work the same.

## Generate

From repo root (or `cd tools/black_collage`):

```bash
# Flattened PNG slides + preview.pptx (best for rundown playback: fonts are baked in)
python3 tools/black_collage/generate_slides.py

# Optional: jitter GIFs + layered teeter PPTX
python3 tools/black_collage/generate_jitter.py

# Editable PPTX (native titles; install the three fonts on the editing Mac)
python3 tools/black_collage/build_editable_pptx.py --out /tmp/memory_collage.pptx
```

Default outputs land next to the scripts (`preview.pptx`, `slide1_childhood.png`, …) and are gitignored.

**Playback vs edit:** `generate_slides.py` rasterizes titles into the slide image, so the party binary does not need the handwriting fonts installed. `build_editable_pptx.py` is for hosts who want to change copy in Keynote/PowerPoint (install Zhi Mang Xing / Ma Shan Zheng, or accept a fallback face).

## Rundown (`kind: ppt`)

`rundown.yaml` at the repo root is the show order. After you generate a deck, copy the `.pptx` to wherever the binary will pack show files (path is yours; do not commit private photos), then declare:

```yaml
- kind: ppt
  path: assets/shows/memory_collage.pptx   # host-chosen path inside the repo/binary
  title: 记忆拼贴
```

Same `{kind, path, title}` shape as video entries (`kind: video`). The Tauri shell is not wired yet; this is the contract from `AGENTS.md`.

See [INTEGRATION_NOTES.md](INTEGRATION_NOTES.md) for a short checklist.

## Fonts

| file | Google Fonts family | role |
| --- | --- | --- |
| `fonts/ZhiMangXing-Regular.ttf` | Zhi Mang Xing | titles |
| `fonts/MaShanZheng-Regular.ttf` | Ma Shan Zheng | labels |
| `fonts/LiuJianMaoCao-Regular.ttf` | Liu Jian Mao Cao | fallback |

Licenses: `fonts/OFL-*.txt` (SIL Open Font License 1.1).
