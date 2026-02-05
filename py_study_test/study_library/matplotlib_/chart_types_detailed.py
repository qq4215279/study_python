# -*- coding: utf-8 -*-
"""
Matplotlib 图表类型详解与进阶技巧

本文件详细介绍各种图表类型的绘制方法和最佳实践
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ChartTypesDetailed:
    """详细图表类型示例"""
    
    @staticmethod
    def time_series_charts():
        """时间序列图表"""
        print("=== 时间序列图表 ===")
        
        # 创建时间序列数据
        # pd.date_range() - pandas函数，创建日期时间范围
        # 参数：起始日期, periods=天数, freq='D'=每日频率
        dates = pd.date_range('2023-01-01', periods=365, freq='D')
        # np.linspace() - 生成线性趋势：从100到200的365个点
        trend = np.linspace(100, 200, 365)
        # 季节性成分：20*sin(2π*天数/365.25) - 模拟年度季节性
        seasonal = 20 * np.sin(2 * np.pi * np.arange(365) / 365.25)
        # 随机噪声：365个正态分布随机数，标准差为5
        noise = np.random.normal(0, 5, 365)
        # 合成数据 = 趋势 + 季节性 + 噪声
        data = trend + seasonal + noise
        
        # plt.subplots() - 创建2行2列的子图布局
        # figsize=(15, 10) - 设置图表尺寸
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        # fig.suptitle() - 设置整个图表的总标题
        fig.suptitle('时间序列图表类型', fontsize=16, fontweight='bold')
        
        # 1. 基础时间序列图
        # axes[0,0] - 访问第一行第一列的子图
        # plot() - 绘制时间序列线图
        # 'b-' - 蓝色实线, linewidth=1 - 线宽, alpha=0.7 - 透明度
        axes[0,0].plot(dates, data, 'b-', linewidth=1, alpha=0.7)
        axes[0,0].set_title('基础时间序列')
        axes[0,0].set_ylabel('数值')
        # grid() - 显示网格线
        axes[0,0].grid(True, alpha=0.3)
        # xaxis.set_major_formatter() - 设置x轴日期格式
        axes[0,0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        # xaxis.set_major_locator() - 设置x轴主刻度间隔
        axes[0,0].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        # 2. 带移动平均的时间序列
        df = pd.DataFrame({'date': dates, 'value': data})
        df['MA_30'] = df['value'].rolling(window=30).mean()
        df['MA_90'] = df['value'].rolling(window=90).mean()
        
        axes[0,1].plot(df['date'], df['value'], 'lightgray', alpha=0.5, label='原始数据')
        axes[0,1].plot(df['date'], df['MA_30'], 'b-', linewidth=2, label='30日移动平均')
        axes[0,1].plot(df['date'], df['MA_90'], 'r-', linewidth=2, label='90日移动平均')
        axes[0,1].set_title('带移动平均的时间序列')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. 分组时间序列
        categories = ['产品A', '产品B', '产品C']
        colors = ['blue', 'red', 'green']
        x_time = pd.date_range('2023-01-01', periods=52, freq='W')
        
        for i, (category, color) in enumerate(zip(categories, colors)):
            values = 100 + i*20 + np.cumsum(np.random.randn(52)) + \
                    10 * np.sin(2*np.pi*np.arange(52)/52)
            axes[1,0].plot(x_time, values, color=color, linewidth=2, 
                          marker='o', markersize=4, label=category)
        
        axes[1,0].set_title('多产品时间序列对比')
        axes[1,0].set_ylabel('销售额')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 4. 时间序列的季节性分解效果
        seasonal_component = seasonal[:100]
        trend_component = trend[:100]
        residual = data[:100] - trend[:100] - seasonal[:100]
        
        x_short = dates[:100]
        axes[1,1].plot(x_short, data[:100], 'black', linewidth=2, label='原始数据', alpha=0.7)
        axes[1,1].plot(x_short, trend[:100], 'blue', linewidth=2, label='趋势')
        axes[1,1].fill_between(x_short, trend[:100] + seasonal[:100], 
                              trend[:100] - seasonal[:100], 
                              alpha=0.3, color='orange', label='季节性范围')
        axes[1,1].set_title('时间序列成分分解')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def distribution_charts():
        """分布图表"""
        print("=== 分布图表 ===")
        
        # 生成不同分布的数据
        np.random.seed(42)
        normal_data = np.random.normal(100, 15, 1000)
        uniform_data = np.random.uniform(80, 120, 1000)
        exponential_data = np.random.exponential(20, 1000) + 80
        bimodal_data = np.concatenate([
            np.random.normal(90, 8, 500),
            np.random.normal(110, 8, 500)
        ])
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('数据分布可视化', fontsize=16, fontweight='bold')
        
        datasets = [normal_data, uniform_data, exponential_data, bimodal_data]
        dataset_names = ['正态分布', '均匀分布', '指数分布', '双峰分布']
        colors = ['blue', 'orange', 'green', 'red']
        
        # 1-4. 不同分布的直方图对比
        for i, (data, name, color) in enumerate(zip(datasets, dataset_names, colors)):
            row, col = i // 3, i % 3
            axes[row, col].hist(data, bins=30, density=True, alpha=0.7, 
                               color=color, edgecolor='black')
            axes[row, col].set_title(f'{name} 直方图')
            axes[row, col].set_xlabel('数值')
            axes[row, col].set_ylabel('密度')
            axes[row, col].grid(True, alpha=0.3)
            
            # 添加统计信息
            mean_val = np.mean(data)
            std_val = np.std(data)
            axes[row, col].axvline(mean_val, color='red', linestyle='--', 
                                 linewidth=2, label=f'均值: {mean_val:.1f}')
            axes[row, col].axvline(mean_val + std_val, color='orange', 
                                 linestyle=':', linewidth=1, alpha=0.7)
            axes[row, col].axvline(mean_val - std_val, color='orange', 
                                 linestyle=':', linewidth=1, alpha=0.7)
            axes[row, col].legend()
        
        # 5. 累积分布函数 (CDF)
        axes[1, 1].clear()
        for data, name, color in zip(datasets, dataset_names, colors):
            sorted_data = np.sort(data)
            y_vals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            axes[1, 1].plot(sorted_data, y_vals, linewidth=2, color=color, label=name)
        axes[1, 1].set_title('累积分布函数 (CDF)')
        axes[1, 1].set_xlabel('数值')
        axes[1, 1].set_ylabel('累积概率')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. QQ图比较
        axes[1, 2].clear()
        from scipy import stats
        stats.probplot(normal_data, dist="norm", plot=axes[1, 2])
        axes[1, 2].set_title('正态QQ图')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def comparative_charts():
        """对比图表"""
        print("=== 对比图表 ===")
        
        # 准备对比数据
        categories = ['Q1', 'Q2', 'Q3', 'Q4']
        product_a = [120, 135, 148, 162]
        product_b = [95, 110, 125, 140]
        product_c = [80, 95, 110, 125]
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('数据对比可视化', fontsize=16, fontweight='bold')
        
        # 1. 分组柱状图
        x = np.arange(len(categories))
        width = 0.25
        
        axes[0, 0].bar(x - width, product_a, width, label='产品A', color='skyblue')
        axes[0, 0].bar(x, product_b, width, label='产品B', color='lightcoral')
        axes[0, 0].bar(x + width, product_c, width, label='产品C', color='lightgreen')
        
        axes[0, 0].set_xlabel('季度')
        axes[0, 0].set_ylabel('销售额 (万元)')
        axes[0, 0].set_title('分组柱状图')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(categories)
        axes[0, 0].legend()
        axes[0, 0].grid(True, axis='y', alpha=0.3)
        
        # 2. 堆叠柱状图
        axes[0, 1].bar(categories, product_a, label='产品A', color='skyblue')
        axes[0, 1].bar(categories, product_b, bottom=product_a, label='产品B', color='lightcoral')
        bottom_values = [a + b for a, b in zip(product_a, product_b)]
        axes[0, 1].bar(categories, product_c, bottom=bottom_values, label='产品C', color='lightgreen')
        
        axes[0, 1].set_xlabel('季度')
        axes[0, 1].set_ylabel('总销售额 (万元)')
        axes[0, 1].set_title('堆叠柱状图')
        axes[0, 1].legend()
        axes[0, 1].grid(True, axis='y', alpha=0.3)
        
        # 3. 水平条形图
        regions = ['华东', '华南', '华北', '华西', '华中']
        sales = [280, 240, 190, 160, 130]
        colors_horizontal = plt.cm.Set3(np.linspace(0, 1, len(regions)))
        
        y_pos = np.arange(len(regions))
        bars = axes[0, 2].barh(y_pos, sales, color=colors_horizontal, alpha=0.8)
        axes[0, 2].set_yticks(y_pos)
        axes[0, 2].set_yticklabels(regions)
        axes[0, 2].set_xlabel('销售额 (万元)')
        axes[0, 2].set_title('各地区销售额')
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars, sales)):
            axes[0, 2].text(value + 5, i, f'{value}', va='center')
        
        axes[0, 2].grid(True, axis='x', alpha=0.3)
        
        # 4. 雷达图
        axes[1, 0] = plt.subplot(2, 3, 4, projection='polar')
        
        metrics = ['性能', '价格', '设计', '服务', '品牌']
        values_a = [4, 3, 5, 4, 3]
        values_b = [3, 5, 3, 5, 4]
        
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        values_a += values_a[:1]  # 闭合图形
        values_b += values_b[:1]
        angles += angles[:1]
        
        axes[1, 0].plot(angles, values_a, 'o-', linewidth=2, label='品牌A', color='blue')
        axes[1, 0].fill(angles, values_a, alpha=0.25, color='blue')
        axes[1, 0].plot(angles, values_b, 's-', linewidth=2, label='品牌B', color='red')
        axes[1, 0].fill(angles, values_b, alpha=0.25, color='red')
        
        axes[1, 0].set_xticks(angles[:-1])
        axes[1, 0].set_xticklabels(metrics)
        axes[1, 0].set_ylim(0, 5)
        axes[1, 0].set_title('产品综合评价雷达图')
        axes[1, 0].legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        # 5. 瀑布图
        axes[1, 1].clear()
        changes = [100, 25, -15, 30, -20, 40]  # 初始值和变化量
        labels = ['初始', '+收入', '-成本', '+投资', '-税费', '+利润']
        colors_waterfall = ['blue'] + ['green' if x > 0 else 'red' for x in changes[1:]]
        
        cumulative = 0
        for i, (change, label, color) in enumerate(zip(changes, labels, colors_waterfall)):
            axes[1, 1].bar(i, change, bottom=cumulative, color=color, alpha=0.7, 
                          edgecolor='black', linewidth=0.5)
            cumulative += change
            axes[1, 1].text(i, cumulative, f'{cumulative}', ha='center', va='bottom')
        
        axes[1, 1].set_xlabel('项目')
        axes[1, 1].set_ylabel('累计金额')
        axes[1, 1].set_title('财务瀑布图')
        axes[1, 1].set_xticks(range(len(labels)))
        axes[1, 1].set_xticklabels(labels, rotation=45)
        axes[1, 1].grid(True, axis='y', alpha=0.3)
        
        # 6. 差异图
        months = ['1月', '2月', '3月', '4月', '5月', '6月']
        actual = [95, 102, 98, 105, 110, 108]
        target = [100, 100, 100, 100, 100, 100]
        differences = [a - t for a, t in zip(actual, target)]
        
        colors_diff = ['green' if x >= 0 else 'red' for x in differences]
        
        x_diff = np.arange(len(months))
        axes[1, 2].bar(x_diff, differences, color=colors_diff, alpha=0.7, 
                      edgecolor='black', linewidth=0.5)
        axes[1, 2].axhline(y=0, color='black', linewidth=1)
        axes[1, 2].set_xlabel('月份')
        axes[1, 2].set_ylabel('差异值')
        axes[1, 2].set_title('目标达成差异图')
        axes[1, 2].set_xticks(x_diff)
        axes[1, 2].set_xticklabels(months)
        axes[1, 2].grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()

class AdvancedTechniques:
    """高级绘图技巧"""
    
    @staticmethod
    def interactive_elements():
        """交互式元素添加"""
        print("=== 交互式元素 ===")
        
        # 创建可交互的图表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 数据准备
        x = np.linspace(0, 10, 100)
        y = np.sin(x) * np.exp(-x/5)
        
        # 主要曲线
        line, = ax.plot(x, y, 'b-', linewidth=2, label='阻尼振荡')
        
        # 添加可点击的点
        highlight_points = [(2, np.sin(2)*np.exp(-2/5)), 
                           (5, np.sin(5)*np.exp(-5/5)),
                           (8, np.sin(8)*np.exp(-8/5))]
        
        for point in highlight_points:
            ax.plot(point[0], point[1], 'ro', markersize=8, 
                   markerfacecolor='red', markeredgecolor='black', 
                   markeredgewidth=2, picker=True)
        
        # 添加注释框
        annotation = ax.annotate('', xy=(0, 0), xytext=(20, 20),
                               textcoords='offset points',
                               bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                               arrowprops=dict(arrowstyle='->'))
        annotation.set_visible(False)
        
        # 添加文本说明
        ax.text(0.02, 0.98, '提示：点击红点查看详细信息', 
               transform=ax.transAxes, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        ax.set_xlabel('时间')
        ax.set_ylabel('振幅')
        ax.set_title('交互式数据探索')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def animation_examples():
        """动画效果示例"""
        print("=== 动画效果示例 ===")
        
        from matplotlib.animation import FuncAnimation
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 初始化数据
        x = np.linspace(0, 4*np.pi, 200)
        line, = ax.plot([], [], 'b-', linewidth=2)
        point, = ax.plot([], [], 'ro', markersize=10)
        
        ax.set_xlim(0, 4*np.pi)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('相位')
        ax.set_ylabel('振幅')
        ax.set_title('正弦波动画演示')
        ax.grid(True, alpha=0.3)
        
        def animate(frame):
            """动画更新函数"""
            y = np.sin(x - frame/10)
            line.set_data(x, y)
            # 移动的点跟随波峰
            peak_idx = np.argmax(y[:50])  # 在前1/4周期找波峰
            point.set_data(x[peak_idx], y[peak_idx])
            return line, point
        
        # 创建动画
        anim = FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
        plt.show()
        
        return anim
    
    @staticmethod
    def style_customization():
        """样式定制"""
        print("=== 样式定制示例 ===")
        
        # 展示不同的内置样式
        styles = ['default', 'seaborn-v0_8', 'ggplot', 'bmh', 'classic']
        
        fig, axes = plt.subplots(1, len(styles), figsize=(20, 4))
        fig.suptitle('不同matplotlib样式的对比', fontsize=16)
        
        x = np.linspace(0, 10, 50)
        y = np.sin(x) + 0.1 * np.random.randn(50)
        
        for i, (style, ax) in enumerate(zip(styles, axes)):
            with plt.style.context(style):
                ax.plot(x, y, 'o-', linewidth=2, markersize=6)
                ax.set_title(f'样式: {style}')
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # 自定义样式示例
        custom_style = {
            'axes.facecolor': '#f8f8f8',
            'axes.edgecolor': 'black',
            'axes.linewidth': 1.2,
            'xtick.direction': 'in',
            'ytick.direction': 'in',
            'xtick.major.size': 6,
            'ytick.major.size': 6,
            'font.size': 12,
            'figure.titlesize': 16,
            'axes.titlesize': 14,
            'axes.labelsize': 12
        }
        
        with plt.rc_context(custom_style):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-o', linewidth=2, markersize=8)
            ax.set_xlabel('X轴标签')
            ax.set_ylabel('Y轴标签')
            ax.set_title('自定义样式示例')
            ax.grid(True, alpha=0.3)
            plt.show()

def main():
    """主函数"""
    print("=" * 60)
    print("Matplotlib 图表类型详解与进阶技巧")
    print("=" * 60)
    
    # 图表类型演示
    chart_demo = ChartTypesDetailed()
    chart_demo.time_series_charts()
    chart_demo.distribution_charts()
    chart_demo.comparative_charts()
    
    # 高级技巧演示
    advanced = AdvancedTechniques()
    advanced.interactive_elements()
    # 注意：动画可能需要额外配置才能正常显示
    # advanced.animation_examples()
    advanced.style_customization()
    
    print("\n所有图表类型示例演示完成！")

if __name__ == "__main__":
    main()