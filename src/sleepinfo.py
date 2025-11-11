import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
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
                'duration': timedelta(minutes=15)
            },
            {
                'time': datetime(2025, 11, 6, 4, 15),
                'duration': timedelta(minutes=10)
            }
        ]
    },
    {
        'date': date(2025, 11, 6),
        'bedtime': datetime(2025, 11, 6, 21, 30),
        'wakeup_time': datetime(2025, 11, 7, 8, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 7, 4, 45),
                'duration': timedelta(minutes=20)
            }
        ]
    },
    {
        'date': date(2025, 11, 7),
        'bedtime': datetime(2025, 11, 7, 22, 15),
        'wakeup_time': datetime(2025, 11, 8, 7, 30),
        'awakenings': [
            {
                'time': datetime(2025, 11, 8, 1, 30),
                'duration': timedelta(minutes=25)
            },
            {
                'time': datetime(2025, 11, 8, 3, 45),
                'duration': timedelta(minutes=15)
            }
        ]
    },
    {
        'date': date(2025, 11, 8),
        'bedtime': datetime(2025, 11, 8, 21, 45),
        'wakeup_time': datetime(2025, 11, 9, 8, 15),
        'awakenings': [
            {
                'time': datetime(2025, 11, 9, 0, 45),
                'duration': timedelta(minutes=10)
            },
            {
                'time': datetime(2025, 11, 9, 4, 30),
                'duration': timedelta(minutes=20)
            }
        ]
    },
    {
        'date': date(2025, 11, 9),
        'bedtime': datetime(2025, 11, 9, 22, 30),
        'wakeup_time': datetime(2025, 11, 10, 9, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 10, 2, 15),
                'duration': timedelta(minutes=15)
            },
            {
                'time': datetime(2025, 11, 10, 3, 30),
                'duration': timedelta(minutes=10)
            },
            {
                'time': datetime(2025, 11, 10, 5, 30),
                'duration': timedelta(minutes=10)
            }
        ]
    },
    {
        'date': date(2025, 11, 10),
        'bedtime': datetime(2025, 11, 10, 22, 10),
        'wakeup_time': datetime(2025, 11, 11, 8, 0),
        'awakenings': [
            {
                'time': datetime(2025, 11, 11, 2, 30),
                'duration': timedelta(minutes=10)
            },
            {
                'time': datetime(2025, 11, 11, 3, 30),
                'duration': timedelta(minutes=10)
            },
            {
                'time': datetime(2025, 11, 11, 5, 45),
                'duration': timedelta(minutes=15)
            }
        ]
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
    
    main_awake_period = "无"
    if night['awakenings']:
        longest_awake = max(night['awakenings'], key=lambda x: x['duration'])
        main_awake_period = longest_awake['time'].strftime('%H:%M')
    
    records.append({
        '日期': date_obj.strftime('%m-%d'),
        '总在床时间(小时)': round(total_sleep, 1),
        '净睡眠时间(小时)': round(net_sleep, 1),
        '夜间醒来次数': num_awakenings,  # 这里已经是整数
        '主要醒来时间': main_awake_period
    })

df = pd.DataFrame(records)

# 确保夜间醒来次数是整数类型
df['夜间醒来次数'] = df['夜间醒来次数'].astype(int)

print("宝宝一周睡眠数据摘要:")
print(df)
print(f"夜间醒来次数的数据类型: {df['夜间醒来次数'].dtype}")

# 创建更合理的图表布局
fig = plt.figure(figsize=(12, 10))
fig.suptitle('BabyOS 睡眠数据分析报告 (v0.7系统)', fontsize=14, fontweight='bold', y=0.98)

# 1. 净睡眠时间趋势图
ax1 = plt.subplot(2, 2, 1)
ax1.plot(df['日期'], df['净睡眠时间(小时)'], marker='o', linewidth=2, markersize=6, color='#4CAF50')
ax1.fill_between(df['日期'], df['净睡眠时间(小时)'], alpha=0.3, color='#4CAF50')
ax1.set_title('净睡眠时间趋势', fontweight='bold', pad=10)
ax1.set_ylabel('小时')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# 2. 夜间醒来次数柱状图 - 设置Y轴为整数刻度
ax2 = plt.subplot(2, 2, 2)
bars = ax2.bar(df['日期'], df['夜间醒来次数'], color='#FF9800', alpha=0.7)
ax2.set_title('夜间醒来次数', fontweight='bold', pad=10)
ax2.set_ylabel('次数')
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

# 设置Y轴为整数刻度
max_awake = df['夜间醒来次数'].max()
ax2.set_yticks(range(0, max_awake + 2))  # 确保Y轴刻度是整数

for bar, v in zip(bars, df['夜间醒来次数']):
    ax2.text(bar.get_x() + bar.get_width()/2, v + 0.05, str(int(v)),  # 确保显示整数
             ha='center', va='bottom', fontweight='bold')

# 3. 睡眠效率饼图
ax3 = plt.subplot(2, 2, 3)
avg_sleep_efficiency = (df['净睡眠时间(小时)'].sum() / df['总在床时间(小时)'].sum()) * 100
other_efficiency = 100 - avg_sleep_efficiency

wedges, texts, autotexts = ax3.pie([avg_sleep_efficiency, other_efficiency], 
                                   labels=['有效睡眠', '醒来时间'], 
                                   autopct='%1.1f%%',
                                   colors=['#2196F3', '#FFC107'],
                                   startangle=90)
ax3.set_title('平均睡眠效率分析', fontweight='bold', pad=10)

# 4. 醒来时间分布图
ax4 = plt.subplot(2, 2, 4)

time_labels = ['20-22', '22-24', '24-02', '02-04', '04-06']
time_ranges = [(20, 22), (22, 24), (0, 2), (2, 4), (4, 6)]

time_awake_count = {label: 0 for label in time_labels}

for night in sleep_data:
    for awakening in night['awakenings']:
        awake_hour = awakening['time'].hour
        for i, (start, end) in enumerate(time_ranges):
            if start <= awake_hour < end or (start > end and (awake_hour >= start or awake_hour < end)):
                time_awake_count[time_labels[i]] += 1
                break

bars = ax4.bar(time_labels, [time_awake_count[label] for label in time_labels], 
               color='#FF5722', alpha=0.7)
ax4.set_title('夜间醒来时间段分布', fontweight='bold', pad=10)
ax4.set_xlabel('时间段')
ax4.set_ylabel('醒来次数')
ax4.grid(True, alpha=0.3)
ax4.tick_params(axis='x', rotation=45)

# 设置Y轴为整数刻度
max_time_awake = max(time_awake_count.values())
ax4.set_yticks(range(0, max_time_awake + 2))

for bar, count in zip(bars, [time_awake_count[label] for label in time_labels]):
    if count > 0:
        ax4.text(bar.get_x() + bar.get_width()/2, count + 0.1, str(count), 
                ha='center', va='bottom', fontweight='bold')

plt.tight_layout(pad=3.0)
plt.show()

# 输出分析结论
print("\n" + "="*50)
print("📊 BabyOS 睡眠分析报告总结:")
print("="*50)
print(f"📍 平均每晚净睡眠: {df['净睡眠时间(小时)'].mean():.1f}小时")
print(f"📍 平均每晚醒来次数: {df['夜间醒来次数'].mean():.1f}次")
print(f"📍 睡眠效率: {avg_sleep_efficiency:.1f}%")

most_common_time = max(time_awake_count, key=time_awake_count.get)
print(f"📍 最需要关注的时段: {most_common_time}点")
print(f"📍 建议: 针对{most_common_time}时段的醒来规律进行重点优化")
print("="*50)