# 麻将牌面

来源：`assets/mahjong/source.jpg`（5行×9列全图，用户上传）。无源图时脚本程序化生成占位牌面。

- 输出：`tiles/` 下 32 张 PNG（tong/tiao/wan 各 1..9 + wind east/south/west/north + dragon_red 红中）
- 尺寸：统一 120×168，透明圆角（R≈14），白底 + 细灰描边
- 切片：单格 W/9 × H/5，内缩 inset 0.045 去黑缝，再 resize + 圆角蒙版
- 运行：`python3 tools/slice_mahjong.py`
