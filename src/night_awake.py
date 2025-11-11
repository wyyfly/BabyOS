import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from matplotlib.colors import ListedColormap  # 添加这个导入
import warnings

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings('ignore')
    
sleep_data = [
    {
        'date': date(2025, 11, 5),
        'bedtime': datetime(2025, 11, 5, 22, 0),
        'wakeup_time': datetime(2025, 11, 6, 8, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 6, 2, 30),
                'duration': timedelta(minutes=15),
                'feeding_ml': 60
            },
            {
                'time': datetime(2025, 11, 6, 4, 15),
                'duration': timedelta(minutes=10),
                'feeding_ml': 60
            }
        ],
        'bedtime_feeding_ml': 150
    },
    {
        'date': date(2025, 11, 6),
        'bedtime': datetime(2025, 11, 6, 21, 30),
        'wakeup_time': datetime(2025, 11, 7, 8, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 7, 4, 45),
                'duration': timedelta(minutes=20),
                'feeding_ml': 60
            }
        ],
        'bedtime_feeding_ml': 150
    },
    {
        'date': date(2025, 11, 7),
        'bedtime': datetime(2025, 11, 7, 22, 15),
        'wakeup_time': datetime(2025, 11, 8, 7, 30),
        'awakenings': [
            {
                'time': datetime(2025, 11, 8, 1, 30),
                'duration': timedelta(minutes=25),
                'feeding_ml': 50
            },
            {
                'time': datetime(2025, 11, 8, 3, 45),
                'duration': timedelta(minutes=15),
                'feeding_ml': 40
            }
        ],
        'bedtime_feeding_ml': 150
    },
    {
        'date': date(2025, 11, 8),
        'bedtime': datetime(2025, 11, 8, 21, 45),
        'wakeup_time': datetime(2025, 11, 9, 8, 15),
        'awakenings': [
            {
                'time': datetime(2025, 11, 9, 0, 45),
                'duration': timedelta(minutes=10),
                'feeding_ml': 120
            }
        ],
        'bedtime_feeding_ml': 150
    },
    {
        'date': date(2025, 11, 9),
        'bedtime': datetime(2025, 11, 9, 22, 30),
        'wakeup_time': datetime(2025, 11, 10, 9, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 10, 2, 15),
                'duration': timedelta(minutes=15),
                'feeding_ml': 80
            },
            {
                'time': datetime(2025, 11, 10, 3, 30),
                'duration': timedelta(minutes=10),
                'feeding_ml': 60
            },
            {
                'time': datetime(2025, 11, 10, 5, 30),
                'duration': timedelta(minutes=10),
                'feeding_ml': 30
            }
        ],
        'bedtime_feeding_ml': 150
    },
    {
        'date': date(2025, 11, 10),
        'bedtime': datetime(2025, 11, 10, 22, 10),
        'wakeup_time': datetime(2025, 11, 11, 8, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 11, 2, 30),
                'duration': timedelta(minutes=10),
                'feeding_ml': 180
            }
        ],
        'bedtime_feeding_ml': 180
    }
]

# 创建DataFrame
records = []
for night in sleep_data:
    date_obj = night['date']
    total_sleep = (night['wakeup_time'] - night['bedtime']).total_seconds() / 3600
    awake_duration = sum((awake['duration'].total_seconds() / 3600) for awake in night['awakenings'])
    net_sleep = total_sleep - awake_duration
    num_awakenings = len(night['awakenings'])
    
    # 计算喂奶相关数据 - 确保是整数
    bedtime_feeding = int(night.get('bedtime_feeding_ml', 0))
    total_night_feeding = int(sum(awake.get('feeding_ml', 0) for awake in night['awakenings']))
    first_feeding_ml = int(night['awakenings'][0].get('feeding_ml', 0)) if night['awakenings'] else 0
    
    main_awake_period = "无"
    if night['awakenings']:
        longest_awake = max(night['awakenings'], key=lambda x: x['duration'])
        main_awake_period = longest_awake['time'].strftime('%H:%M')
    
    # 判断是否一觉到天亮
    sleep_through = (num_awakenings == 1 and night['awakenings'][0]['time'].hour <= 3)
    
    records.append({
        '日期': date_obj.strftime('%m-%d'),
        '总在床时间(小时)': round(total_sleep, 1),
        '净睡眠时间(小时)': round(net_sleep, 1),
        '夜间醒来次数': num_awakenings,
        '睡前奶量(ml)': bedtime_feeding,
        '夜间总喂奶量(ml)': total_night_feeding,
        '第一次夜醒喂奶量(ml)': first_feeding_ml,
        '主要醒来时间': main_awake_period,
        '一觉到天亮': '是' if sleep_through else '否'
    })

df = pd.DataFrame(records)
df['夜间醒来次数'] = df['夜间醒来次数'].astype(int)

print("宝宝一周睡眠饮食数据摘要:")
print(df)
print(f"\n数据类型检查:")
print(df[['睡前奶量(ml)', '夜间总喂奶量(ml)', '第一次夜醒喂奶量(ml)']].dtypes)

# 正确的相关性分析
print(f"\n数据相关性分析:")
corr_matrix = df[['睡前奶量(ml)', '第一次夜醒喂奶量(ml)', '夜间醒来次数', '净睡眠时间(小时)']].corr()
print(corr_matrix.round(3))

# 创建图表布局
fig = plt.figure(figsize=(16, 12))
fig.suptitle('BabyOS 睡眠饮食关联分析报告 (v0.9系统优化版)', fontsize=16, fontweight='bold', y=0.98)

# 1. 睡前奶量与夜间醒来次数的关系
ax1 = plt.subplot(2, 3, 1)
scatter = ax1.scatter(df['睡前奶量(ml)'], df['夜间醒来次数'], c=df['净睡眠时间(小时)'], 
                     cmap='viridis', s=100, alpha=0.7)
ax1.set_xlabel('睡前奶量 (ml)')
ax1.set_ylabel('夜间醒来次数')
ax1.set_title('睡前奶量 vs 夜间醒来次数\n(颜色深浅表示睡眠时长)', fontweight='bold', pad=10)
ax1.grid(True, alpha=0.3)

# 添加颜色条
cbar = plt.colorbar(scatter, ax=ax1)
cbar.set_label('净睡眠时间(小时)')

# 添加趋势线
z = np.polyfit(df['睡前奶量(ml)'], df['夜间醒来次数'], 1)
p = np.poly1d(z)
ax1.plot(df['睡前奶量(ml)'], p(df['睡前奶量(ml)']), "r--", alpha=0.8, label='趋势线')
ax1.legend()

# 2. 第一次夜醒喂奶量与后续睡眠的关系
ax2 = plt.subplot(2, 3, 2)
colors = ['green' if x == '是' else 'red' for x in df['一觉到天亮']]
scatter2 = ax2.scatter(df['第一次夜醒喂奶量(ml)'], df['夜间醒来次数'], c=colors, s=100, alpha=0.7)
ax2.set_xlabel('第一次夜醒喂奶量 (ml)')
ax2.set_ylabel('夜间醒来次数')
ax2.set_title('第一次喂奶量 vs 后续睡眠质量\n(绿色=一觉到天亮)', fontweight='bold', pad=10)
ax2.grid(True, alpha=0.3)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='green', label='一觉到天亮'),
                   Patch(facecolor='red', label='多次醒来')]
ax2.legend(handles=legend_elements)

# 3. 夜间醒来次数趋势
ax3 = plt.subplot(2, 3, 3)
bars = ax3.bar(df['日期'], df['夜间醒来次数'], 
               color=['#FF6B6B' if x > 1 else '#51CF66' for x in df['夜间醒来次数']], 
               alpha=0.7)
ax3.set_title('夜间醒来次数趋势\n(红色>1次, 绿色≤1次)', fontweight='bold', pad=10)
ax3.set_ylabel('次数')
ax3.grid(True, alpha=0.3)
ax3.tick_params(axis='x', rotation=45)
ax3.set_yticks(range(0, df['夜间醒来次数'].max() + 2))

for bar, v in zip(bars, df['夜间醒来次数']):
    ax3.text(bar.get_x() + bar.get_width()/2, v + 0.05, str(int(v)), 
             ha='center', va='bottom', fontweight='bold')

# 4. 喂奶量对比
ax4 = plt.subplot(2, 3, 4)
x = np.arange(len(df))
width = 0.35
bars1 = ax4.bar(x - width/2, df['睡前奶量(ml)'], width, label='睡前奶量', alpha=0.7, color='#4ECDC4')
bars2 = ax4.bar(x + width/2, df['夜间总喂奶量(ml)'], width, label='夜间总喂奶量', alpha=0.7, color='#FF9F1C')
ax4.set_xlabel('日期')
ax4.set_ylabel('奶量 (ml)')
ax4.set_title('睡前 vs 夜间喂奶量对比', fontweight='bold', pad=10)
ax4.set_xticks(x)
ax4.set_xticklabels(df['日期'])
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.tick_params(axis='x', rotation=45)

# 5. 睡眠效率与喂奶量关系
ax5 = plt.subplot(2, 3, 5)
scatter3 = ax5.scatter(df['睡前奶量(ml)'], df['净睡眠时间(小时)'], 
                      c=df['第一次夜醒喂奶量(ml)'], s=100, alpha=0.7, cmap='plasma')
ax5.set_xlabel('睡前奶量 (ml)')
ax5.set_ylabel('净睡眠时间 (小时)')
ax5.set_title('喂奶量与睡眠时长关系\n(颜色=第一次喂奶量)', fontweight='bold', pad=10)
ax5.grid(True, alpha=0.3)
cbar3 = plt.colorbar(scatter3, ax=ax5)
cbar3.set_label('第一次喂奶量(ml)')

# 6. 优化建议矩阵（修正版）
ax6 = plt.subplot(2, 3, 6)

# 创建优化建议矩阵
factors = ['睡前奶量≥150ml', '第一次喂奶≥100ml', '夜间醒来≤1次']
success_matrix = []

for i, row in df.iterrows():
    day_factors = []
    day_factors.append(1 if row['睡前奶量(ml)'] >= 150 else 0)
    day_factors.append(1 if row['第一次夜醒喂奶量(ml)'] >= 100 else 0)
    day_factors.append(1 if row['夜间醒来次数'] <= 1 else 0)
    success_matrix.append(day_factors)

success_matrix = np.array(success_matrix).T

# 修正：使用 ListedColormap
custom_cmap = ListedColormap(['red', 'green'])
im = ax6.imshow(success_matrix, cmap=custom_cmap, aspect='auto', vmin=0, vmax=1)

ax6.set_xticks(range(len(df)))
ax6.set_xticklabels(df['日期'])
ax6.set_yticks(range(3))
ax6.set_yticklabels(factors)
ax6.set_title('睡眠优化因素分析\n(绿色=达标, 红色=未达标)', fontweight='bold', pad=10)

# 添加数值标注
for i in range(3):
    for j in range(len(df)):
        color = 'white' if success_matrix[i, j] == 1 else 'black'
        ax6.text(j, i, '✓' if success_matrix[i, j] == 1 else '✗', 
                ha='center', va='center', fontsize=14, fontweight='bold', color=color)

# 添加网格线
ax6.set_xticks(np.arange(-0.5, len(df), 1), minor=True)
ax6.set_yticks(np.arange(-0.5, 3, 1), minor=True)
ax6.grid(which="minor", color="black", linestyle='-', linewidth=0.8)
ax6.tick_params(which="minor", bottom=False, left=False)

plt.tight_layout(pad=3.0)
plt.show()

# 输出分析结论
print("\n" + "="*60)
print("📊 BabyOS 睡眠饮食关联分析报告总结:")
print("="*60)

# 计算正确的相关性
corr_bedtime_awake = df['睡前奶量(ml)'].corr(df['夜间醒来次数'])
corr_first_feeding_awake = df['第一次夜醒喂奶量(ml)'].corr(df['夜间醒来次数'])
corr_bedtime_sleep = df['睡前奶量(ml)'].corr(df['净睡眠时间(小时)'])

print(f"📍 睡前奶量与夜间醒来次数的相关性: {corr_bedtime_awake:.3f}")
print(f"📍 第一次夜醒喂奶量与总醒来次数的相关性: {corr_first_feeding_awake:.3f}")
print(f"📍 睡前奶量与净睡眠时长的相关性: {corr_bedtime_sleep:.3f}")
print(f"📍 平均睡前奶量: {df['睡前奶量(ml)'].mean():.0f}ml")
print(f"📍 平均夜间喂奶量: {df['夜间总喂奶量(ml)'].mean():.0f}ml")

# 给出具体建议
best_night = df[df['夜间醒来次数'] == df['夜间醒来次数'].min()].iloc[0]
print(f"\n📍 最佳实践参考 ({best_night['日期']}):")
print(f"   - 睡前奶量: {best_night['睡前奶量(ml)']}ml")
print(f"   - 第一次夜醒喂奶: {best_night['第一次夜醒喂奶量(ml)']}ml")
print(f"   - 夜间醒来次数: {best_night['夜间醒来次数']}次")

print("\n💡 优化建议:")
if corr_bedtime_awake < -0.3:
    print("   ✅ 增加睡前奶量可能有助于减少夜醒")
else:
    print("   ℹ️  睡前奶量与夜醒次数关联不明显")
    
if corr_first_feeding_awake < -0.3:
    print("   ✅ 第一次夜醒时适当增加喂奶量可能改善后续睡眠")
else:
    print("   ℹ️  第一次喂奶量与后续睡眠关联不明显")

# 分析优化因素矩阵
print(f"\n📈 达标情况统计:")
print(f"   - 睡前奶量达标天数: {sum(df['睡前奶量(ml)'] >= 150)}/{len(df)}")
print(f"   - 第一次喂奶达标天数: {sum(df['第一次夜醒喂奶量(ml)'] >= 100)}/{len(df)}")
print(f"   - 睡眠质量达标天数: {sum(df['夜间醒来次数'] <= 1)}/{len(df)}")
print("="*60)