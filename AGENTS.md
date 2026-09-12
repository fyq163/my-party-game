# Repository Guidelines

## Product Direction

- 大屏幕派对游戏库，发版形态是本机 portable 二进制（macOS 先行）。
- 技术栈：Tauri + Web 前端。现有 Python/tkinter 牌面代码是资产沉淀（牌面 PNG 生成逻辑可复用），
  新功能（menu、编排、游戏）用前端实现；Python 侧不再新增 GUI。
- 二进制 = menu + 编排 + 游戏。`rundown.yaml`（仓库根）是节目单唯一入口，
  按顺序声明 `game | ppt | video` 条目；视频/PPT 打进二进制，用条目里的 `path` 引用。
- 里程碑 1：menu + 第一个游戏“麻将胡什么”（给一副手牌，猜胡什么）。
  游戏 PRD 见 `games/mahjong_hu_shenme/prd.md`（规则/玩法/design 由用户填写）。

## Repo Map (verified)

- `games/mahjong_hand/main.py` — 旧 tkinter 手牌展示（已冻结，不再扩展）。
  牌面来源以 `assets/mahjong/manifest.json` 为准；验证用
  `python3 games/mahjong_hand/main.py --count 12 --save output/hand.png`（免开窗）。
- `games/mahjong_hu_shenme/prd.md` — 第一个游戏的 PRD，骨架已搭好，内容待补。
- `tools/slice_mahjong.py` — 牌面生成器，`TILES` 是 32 张牌的唯一真实来源。
  特殊牌面归它所有：七筒 3 上 4 下、八筒 2 列×4 行、八条上下对称 M。
  运行：`python3 tools/slice_mahjong.py`（需 Pillow）。
- `assets/mahjong/tiles/*.png` — 120×168 统一尺寸；牌面汉字用楷体（LXGW WenKai，中宫大），
  字体放本机 `assets/private/fonts/`（已 ignore，各生成机自备，`~/Library/Fonts` 也装了一份），
  缺字体时回退系统黑体。
- `rundown.yaml` — 节目单（待建）。条目暂定 `{kind, path|game, title}`，
  定稿前 `games/` 下不新增顶层概念。

## Conventions / Gotchas

- 加新牌必须同时改两处：`tools/slice_mahjong.py` 的 `TILES`（含 source.jpg 切片行列）
  和游戏侧的排序映射（Python 侧是 `SUIT_ORDER`，前端建好后在此登记对应文件）。
- 牌面 PNG 白底细灰描边、透明圆角 R≈14，改风格时整套一起重生成，别单改一张。
- Agent 验证一律走 headless（`--save` / 构建产物），不准弹 Tk 窗口。
- 不提交：`__pycache__/`、`output/`、`assets/private/`（个人实拍 `source.jpg`、自带字体都在里面）、凭据。
- 依赖尚未落盘（只有 Pillow）：`python3 -m pip install Pillow`；`requirements.txt` 待补。

## Style

- Python 旧代码：4 空格、UTF-8、PEP 8 命名，GUI 逻辑与规则分离（沿用现有模式）。
- 新前端代码规范等 Tauri 脚手架落定后再补一节，不提前编造命令。
