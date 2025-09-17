import matplotlib.pyplot as plt
import numpy as np

# 正規化データ (0〜1 = 24時間、エクセルでは時刻データ入力後にセルの書式設定を標準にすることで正規化した値に変換する)
data = {
    "day":     [0.25,0.260416667,0.263888889],
    "night":   [0.791666667,0.805555556,0.791666667,0.833333333,0.798611111,0.777777778,0.819444444],
    "hybrid":  [1.013888889,0.996527778,0.979166667,0.996527778]
}

# 色分け
colors = {"day":"red", "night":"blue", "hybrid":"green"}

# ← ここは subplots だけに統一！
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6,6))

# 暗期の時間帯：18:00〜翌8:00
night_start = 18
night_end = 8

theta_start = night_start / 24 * 2*np.pi
theta_end   = night_end / 24 * 2*np.pi

thetas1 = np.linspace(theta_start, 2*np.pi, 100, endpoint=False)
thetas2 = np.linspace(0, theta_end, 100, endpoint=True)

ax.fill_between(thetas1, 0, 1.05, color="lightgray", alpha=0.3)
ax.fill_between(thetas2, 0, 1.05, color="lightgray", alpha=0.3)

for group, values in data.items():
    angles = np.array(values) * 2 * np.pi

    # 散布図
    ax.scatter(angles, [1]*len(angles),
               label=group, color=colors[group], s=40, alpha=0.7)

    # ベクトル平均
    mean_x = np.mean(np.cos(angles))
    mean_y = np.mean(np.sin(angles))
    mean_angle = np.arctan2(mean_y, mean_x)
    R = np.sqrt(mean_x**2 + mean_y**2)

    # 平均ベクトル描画
    ax.arrow(mean_angle, 0, 0, R,
             width=0.015, head_width=0.08, head_length=0.1,
             color=colors[group], alpha=0.8, length_includes_head=True)

    # 平均時刻ラベルを矢印の近くに表示
    mean_hour = (mean_angle / (2*np.pi) * 24) % 24
    hour_int = int(mean_hour)
    minute_int = int((mean_hour - hour_int) * 60)
    label = f"{hour_int:02d}:{minute_int:02d}"

    ax.text(mean_angle, R*0.75, label, color=colors[group],
            fontsize=11, fontname="DejaVu Sans", ha="center", va="bottom")

# 時計盤の目盛り（2時間ごと）
hours = np.arange(0, 24, 2)
ax.set_xticks(np.linspace(0, 2*np.pi, len(hours), endpoint=False))
ax.set_xticklabels([f"{h}:00" for h in hours], fontname="DejaVu Sans")

# 0時を上に、時計回り
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# 半径ラベルを消す
ax.set_yticks([])

# タイトル
ax.set_title("メキシコアサガオ開花時刻 (8-18時,10L14D)（分布、同期度ベクトル＋平均時刻）",
             va="bottom", fontname="Hiragino Sans", fontsize=14)

# 凡例（円グラフと重ならない位置）
ax.legend(loc="upper left", bbox_to_anchor=(0.9, 1.0))

plt.show()
