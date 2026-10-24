import os
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. 数据下载与读取 ----------
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, 'ersst5_nino34.txt')
DATA_URL = 'https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.81-10.ascii'
if not os.path.exists(DATA_FILE):
    urllib.request.urlretrieve(DATA_URL, DATA_FILE)
    print('已下载数据:', DATA_FILE)

COLS = ['yr', 'mon', 'nino12', 'a12', 'nino3', 'a3', 'nino4', 'a4', 'nino34', 'a34']
frame = pd.read_fwf(DATA_FILE, header=0, names=COLS)
frame = frame[(frame.yr >= 1950) & (frame.yr <= 1995)].reset_index(drop=True)

t = np.arange(len(frame))
nino = frame.a34.astype(float).values
years, months = frame.yr.values, frame.mon.values

# ---------- 2. 自测模块 ----------
print('=' * 56)
print('自测试模块')
print(f'样本数     {len(frame)}（应为 552：1950.1~1995.12）')
print(f'时间范围   {years[0]}.{months[0]:02d} ~ {years[-1]}.{months[-1]:02d}')
print(f'异常值     [{nino.min():.2f}, {nino.max():.2f}] °C')
print(f'缺测数     {(nino == -99.9).sum()}')
print(f'El Niño 月  {(nino >= 0.5).sum()}（>+0.5°C）  La Niña 月 {(nino <= -0.5).sum()}（<-0.5°C）')
print('=' * 56)

# ---------- 3. 绘图 ----------
plt.rcParams['font.size'] = 11
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6.8), sharex=True, facecolor='white')
fig.subplots_adjust(hspace=0.3)

THR, TEAL = 0.5, '#4682B4'
xlab_mask = (months == 1) & np.isin(years, np.arange(1950, 1996, 5))
xpos, xlab = t[xlab_mask], years[xlab_mask].astype(str)

for ax in (ax1, ax2):                      # 两幅图共用坐标样式
    ax.set_yticks(np.arange(-2.5, 3.0, 0.5))
    ax.set_ylim(-2.5, 2.5)
    ax.set_ylabel('SST Anomaly (°C)')
    ax.axhline(0, color='black', lw=0.9)
    ax.grid(alpha=0.3)

ax1.set_title('Niño 3.4 SST Anomaly Time Series', fontsize=13)
ax1.plot(t, nino, color=TEAL, lw=1.1, label='Niño 3.4 SST Anomaly')
ax1.fill_between(t, 0, nino, color='grey', alpha=0.55)
ax1.legend(loc='upper right', frameon=False)
plt.setp(ax1.get_xticklabels(), visible=False)

ax2.set_title('El Niño (Red) / La Niña (Blue) Phases', fontsize=13)
ax2.plot(t, nino, color='black', lw=0.9)
ax2.fill_between(t, THR, nino, where=nino >= THR, color='red', alpha=0.8,
                 label='El Niño (warm)')
ax2.fill_between(t, -THR, nino, where=nino <= -THR, color='blue', alpha=0.8,
                 label='La Niña (cold)')
ax2.axhline(THR, color='red', ls='--', lw=0.9)
ax2.axhline(-THR, color='blue', ls='--', lw=0.9)
ax2.set_xlabel('Year')
ax2.set_xticks(xpos)
ax2.set_xticklabels(xlab)
ax2.legend(loc='upper right', frameon=False)

# ---------- 4. 保存与显示 ----------
OUT = os.path.join(HERE, 'enso_time_series.png')
plt.savefig(OUT, dpi=300, bbox_inches='tight')
print('\n图像已保存:', OUT)
plt.show()