# enso-timeseries-plot

ENSO（Niño 3.4）海温距平时间序列绘图小工具：自动下载 NOAA CPC 官方数据，
内置自测模块校验数据质量，生成两联可视化图（时间序列 + El Niño/La Niña 位相着色）。

## 功能

1. **数据管道**：首次运行自动下载 NOAA CPC ERSST5 Niño 指数月值数据
   （[ersst5.nino.mth.81-10.ascii](https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.81-10.ascii)），
   之后复用本地缓存，离线也可运行；
2. **自测模块**：读取后立即打印样本数、时间范围、异常值范围、缺测数、
   El Niño / La Niña 月数等质量统计（预期值一并给出，方便核对）；
3. **可视化**：生成 `enso_time_series.png`（300 dpi）：
   - 上图：Niño 3.4 海温距平时间序列（1950–1995）；
   - 下图：以 ±0.5 °C 阈值着色的 El Niño（红）/ La Niña（蓝）位相。

## 运行

环境要求：Python 3.8+，依赖 `numpy` / `pandas` / `matplotlib`。

```bash
pip install numpy pandas matplotlib
python enso_timeseries.py
```

首次运行会自动下载数据文件 `ersst5_nino34.txt` 到脚本所在目录；
运行结束在当前目录生成 `enso_time_series.png` 并弹出预览窗口。

## 自测输出示例

```
========================================================
自测试模块
样本数     552（应为 552：1950.1~1995.12）
时间范围   1950.01 ~ 1995.12
异常值     [-2.37, 2.34] °C
缺测数     0
El Niño 月  113（>+0.5°C）  La Niña 月 203（<-0.5°C）
========================================================
图像已保存: ...\enso_time_series.png
```

## 说明

- 图中 ±0.5 °C 单月阈值是**教学演示用的简化判定**；业务上 NOAA 官方以
  ONI（Niño 3.4 三个月滑动平均 ≥ +0.5 °C 且持续 5 个月）判定 ENSO 事件，
  二者在边界月份会有差异；
- 数据区间 1950–1995 为脚本示例设置，修改 `frame` 筛选条件即可调整；
- 异常值 -99.9 为 NOAA 的缺测记号，自测模块会统计其数量。

## 文件结构

```
enso-timeseries-plot/
├── enso_timeseries.py      # 主程序（下载 + 自测 + 绘图）
├── README.md
└── .gitignore              # 忽略下载的数据与生成图像
```