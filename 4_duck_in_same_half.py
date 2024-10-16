import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 全局變數
NUM_DUCKS = 4
successful_trials = 0
total_trials = 0
MAX_TRIALS = 1000  # 設定最大試驗次數

# 創建畫布
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

# 畫一個圓代表池塘
circle = plt.Circle((0, 0), 1, color='blue', fill=False)
ax.add_artist(circle)

# 創建文字物件來顯示概率
prob_text = plt.text(0, 1.2, "", ha="center", va="center", fontsize=12, color="blue")

# 鴨子的初始位置
ducks, = ax.plot([], [], 'ro')

# 更新函數
def update(frame):
    global successful_trials, total_trials

#     # 生成隨機的鴨子角度
#     angles = np.random.rand(NUM_DUCKS) * 2 * np.pi
#     x_coords = np.cos(angles)
#     y_coords = np.sin(angles)
# 
#     # 判斷這些鴨子是否都在同一個半圓內
#     in_half_circle = np.max(angles) - np.min(angles) <= np.pi
#  上述方法是chatGPT在多次對話後給的答案
#  下面方法是chatGPT一開始給的答案 但下面方法才是對的 他有處理跨越2pi的問題
    # 隨機生成鴨子在圓周上的角度 [0, 2*pi)
    angles = np.random.uniform(0, 2*np.pi, NUM_DUCKS)
    x_coords = np.cos(angles)
    y_coords = np.sin(angles)
    # 計算這些角度的範圍
    angles.sort()
    max_gap = np.max(np.diff(np.concatenate([angles, angles[:1] + 2*np.pi])))
    # 如果最大間隔小於 pi，則所有鴨子在同一半圓內
    in_half_circle = (max_gap >= np.pi)

    # 更新試驗次數
    total_trials += 1
    if in_half_circle:
        successful_trials += 1

    # 計算當前的成功率（即鴨子都位於同一個半圓內的概率）
    current_probability = successful_trials / total_trials

    # 更新鴨子的位置
    ducks.set_data(x_coords, y_coords)

    # 更新顯示的概率
    prob_text.set_text(f"Current Probability: {in_half_circle} {current_probability:.4f} / {total_trials} ")

    # 如果達到最大試驗次數，結束動畫
    if total_trials >= MAX_TRIALS:
        plt.waitforbuttonpress()
        plt.close()

# 動畫設置
ani = FuncAnimation(fig, update, frames=np.arange(0, MAX_TRIALS), interval=1500, blit=False)

plt.show()
