# Mahjong Hand（纯展示）

11/12 张牌组合陈列，无交互（线下交互）。

```bash
python3 games/mahjong_hand/main.py                 # 随机 11 张展示
python3 games/mahjong_hand/main.py --count 12 --seed 7
python3 games/mahjong_hand/main.py --hand tong_1,tong_1,tiao_5,wan_9,wind_east
python3 games/mahjong_hand/main.py --count 12 --save output/hand.png  # 拼图免开窗
python3 -m games.mahjong_hand.main --count 12 --save output/hand.png
```
