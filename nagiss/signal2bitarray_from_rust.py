import math
from scipy.io import wavfile

sample_rate, samples = wavfile.read(r"radio-transmission-recording.wav")

freq = 600
step = 2.0 * math.pi * freq / sample_rate  # 周期 / サンプル　逆数は 1 周期のサンプル数
xys = []  # 90°ずれた 2 つの周波数 freq の正弦波との要素ごとの積
for i, s in enumerate(samples):
    a = i * step  # 位相
    xys.append((math.cos(a) * s, math.sin(a) * s))

axyz = [(0.0, 0.0)]  # xys の累積和
for x, y in xys:
    x_old, y_old = axyz[-1]
    axyz.append((x + x_old, y + y_old))

ds = []
for xy1, xy2 in zip(axyz, axyz[1000:]):  # 1000 サンプルずらして自己相関を見てる？
    dx = xy1[0] - xy2[0]
    dy = xy1[1] - xy2[1]
    ds.append(dx * dx + dy * dy)

max_ = max(ds)
for i in range(len(ds)):
    ds[i] /= max_

width = 100
height = 195

mat = [[0]*width for _ in range(height)]
for y in range(height):
    for x in range(width):
        d =  ds[(x + y//4 * width) * 529 + 132400]
        mat[y][x] = d

# 描画
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 8))
plt.imshow(mat,interpolation='nearest',cmap='jet',aspect=1)
plt.show()

