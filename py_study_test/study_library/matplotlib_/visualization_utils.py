# -*- coding: utf-8 -*-
"""
Matplotlib 实用工具类和最佳实践

包含常用的图表模板、样式预设和实用函数
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Union
import seaborn as sns
from datetime import datetime, timedelta

# 设置全局样式和中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8')  # 使用现代化样式

class PlotTemplates:
    """常用图表模板类"""
    
    @staticmethod
    def clean_line_chart(x_data, y_data, title="", xlabel="", ylabel="", 
                        color='blue', figsize=(10, 6)):
        """
        清晰简洁的折线图模板
        
        Parameters:
        -----------
        x_data : array-like
            X轴数据
        y_data : array-like  
            Y轴数据
        title : str
            图表标题
        xlabel : str
            X轴标签
        ylabel : str
            Y轴标签
        color : str
            线条颜色
        figsize : tuple
            图表大小
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # 绘制主要线条
        ax.plot(x_data, y_data, color=color, linewidth=2.5, marker='o', 
                markersize=6, markerfacecolor='white', markeredgewidth=2)
        
        # 美化设置
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        
        # 网格和背景
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#fafafa')
        
        # 边框设置
        for spine in ax.spines.values():
            spine.set_linewidth(0.5)
        
        plt.tight_layout()
        return fig, ax
    
    @staticmethod
    def professional_bar_chart(categories, values, title="", xlabel="", ylabel="",
                             colors=None, figsize=(10, 6), horizontal=False):
        """
        专业的柱状图模板
        
        Parameters:
        -----------
        categories : list
            类别标签
        values : array-like
            数值数据
        title : str
            图表标题
        xlabel : str
            X轴标签
        ylabel : str
            Y轴标签
        colors : list or str
            颜色设置
        figsize : tuple
            图表大小
        horizontal : bool
            是否水平柱状图
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # 颜色处理
        if colors is None:
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        elif isinstance(colors, str):
            colors = [colors] * len(categories)
        
        # 绘制柱状图
        if horizontal:
            bars = ax.barh(range(len(categories)), values, color=colors, alpha=0.8)
            ax.set_yticks(range(len(categories)))
            ax.set_yticklabels(categories)
            ax.set_ylabel(ylabel)
            ax.set_xlabel(xlabel)
        else:
            bars = ax.bar(categories, values, color=colors, alpha=0.8)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.xticks(rotation=45, ha='right')
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars, values)):
            if horizontal:
                ax.text(value + max(values)*0.01, i, f'{value:.1f}', 
                       va='center', fontweight='bold')
            else:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                       f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 美化设置
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, axis='y' if not horizontal else 'x', alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        plt.tight_layout()
        return fig, ax
    
    @staticmethod
    def elegant_pie_chart(sizes, labels, title="", colors=None, figsize=(8, 8)):
        """
        优雅的饼图模板
        
        Parameters:
        -----------
        sizes : list
            各部分大小
        labels : list
            标签
        title : str
            图表标题
        colors : list
            颜色列表
        figsize : tuple
            图表大小
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if colors is None:
            colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                         autopct='%1.1f%%', startangle=90,
                                         textprops={'fontsize': 10})
        
        # 美化文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('equal')  # 确保圆形
        
        plt.tight_layout()
        return fig, ax
    
    @staticmethod
    def statistical_box_plot(data_dict, title="", xlabel="", ylabel="", 
                           figsize=(10, 6)):
        """
        统计箱线图模板
        
        Parameters:
        -----------
        data_dict : dict
            {'组名': [数据列表]} 格式的数据字典
        title : str
            图表标题
        xlabel : str
            X轴标签
        ylabel : str
            Y轴标签
        figsize : tuple
            图表大小
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        labels = list(data_dict.keys())
        data = list(data_dict.values())
        
        # 创建箱线图
        box_plot = ax.boxplot(data, labels=labels, patch_artist=True,
                             notch=True,  # 凹槽样式
                             boxprops=dict(facecolor='lightblue', alpha=0.7),
                             medianprops=dict(color='red', linewidth=2),
                             whiskerprops=dict(linewidth=1.5),
                             capprops=dict(linewidth=1.5))
        
        # 美化设置
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        plt.tight_layout()
        return fig, ax

class DataVisualizationUtils:
    """数据可视化工具类"""
    
    @staticmethod
    def create_correlation_heatmap(dataframe, title="相关性热力图", 
                                 figsize=(10, 8), annot=True):
        """
        创建相关性热力图
        
        Parameters:
        -----------
        dataframe : pd.DataFrame
            数据框
        title : str
            图表标题
        figsize : tuple
            图表大小
        annot : bool
            是否显示数值
        """
        # 计算相关系数矩阵
        corr_matrix = dataframe.corr()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # 创建热力图
        im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
        
        # 设置标签
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr_matrix.columns)
        
        # 添加数值标注
        if annot:
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                 ha="center", va="center", color="black",
                                 fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.colorbar(im, ax=ax)
        plt.tight_layout()
        return fig, ax
    
    @staticmethod
    def time_series_decomposition(dates, values, title="时间序列分解", 
                                figsize=(12, 10)):
        """
        时间序列分解图（趋势、季节性、残差）
        
        Parameters:
        -----------
        dates : array-like
            时间数据
        values : array-like
            数值数据
        title : str
            图表标题
        figsize : tuple
            图表大小
        """
        fig, axes = plt.subplots(4, 1, figsize=figsize, sharex=True)
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # 原始数据
        axes[0].plot(dates, values, 'b-', linewidth=1, alpha=0.7)
        axes[0].set_ylabel('原始数据')
        axes[0].grid(True, alpha=0.3)
        
        # 趋势（移动平均）
        window = min(30, len(values)//4)  # 动态窗口大小
        trend = pd.Series(values).rolling(window=window).mean()
        axes[1].plot(dates, trend, 'r-', linewidth=2)
        axes[1].set_ylabel('趋势')
        axes[1].grid(True, alpha=0.3)
        
        # 季节性（去趋势后的数据）
        if len(values) > window:
            detrended = values - trend
            seasonal_window = min(12, len(detrended)//2)
            seasonal = pd.Series(detrended).rolling(window=seasonal_window, center=True).mean()
            axes[2].plot(dates, seasonal, 'g-', linewidth=1.5)
            axes[2].set_ylabel('季节性')
            axes[2].grid(True, alpha=0.3)
        
        # 残差
        if len(values) > window:
            residual = values - trend - seasonal
            axes[3].plot(dates, residual, 'purple', linewidth=0.8, alpha=0.7)
            axes[3].set_ylabel('残差')
            axes[3].set_xlabel('时间')
            axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig, axes
    
    @staticmethod
    def multi_axis_plot(x_data, y_datasets, title="", xlabel="", figsize=(12, 6)):
        """
        多Y轴对比图
        
        Parameters:
        -----------
        x_data : array-like
            X轴数据
        y_datasets : list of tuples
            [('标签', 数据, '颜色', 'Y轴位置')] 的列表
            Y轴位置: 'left' 或 'right'
        title : str
            图表标题
        xlabel : str
            X轴标签
        figsize : tuple
            图表大小
        """
        fig, ax1 = plt.subplots(figsize=figsize)
        
        # 创建第二个Y轴
        ax2 = ax1.twinx()
        
        axes = {'left': ax1, 'right': ax2}
        colors_used = []
        
        for label, data, color, y_side in y_datasets:
            ax = axes[y_side]
            line = ax.plot(x_data, data, color=color, linewidth=2, 
                          marker='o', markersize=4, label=label)
            colors_used.append(line[0])
        
        # 设置标签
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel('左侧Y轴', color='blue')
        ax2.set_ylabel('右侧Y轴', color='red')
        
        # 设置颜色
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='red')
        
        ax1.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax1.grid(True, alpha=0.3)
        
        # 合并图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        return fig, (ax1, ax2)

class BestPracticesDemo:
    """最佳实践演示"""
    
    @staticmethod
    def before_after_comparison():
        """前后对比示例 - 展示好的vs不好的做法"""
        print("=== 图表设计最佳实践对比 ===")
        
        # 生成示例数据
        categories = ['产品A', '产品B', '产品C', '产品D']
        before_values = [25, 30, 35, 20]
        after_values = [45, 38, 42, 35]
        
        # 不好的做法
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bad example - 设计糟糕的图表
        ax1.bar(range(len(categories)), before_values, color='blue', alpha=0.7)
        ax1.bar(range(len(categories)), after_values, color='red', alpha=0.7)
        ax1.set_title('❌ 设计糟糕的对比图', fontsize=14)
        ax1.set_xticks(range(len(categories)))
        ax1.set_xticklabels(categories)
        # 缺少标签、网格、适当的间距等
        
        # Good example - 设计良好的图表
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, before_values, width, label='改进前', 
                       color='#ff9999', alpha=0.8, edgecolor='black')
        bars2 = ax2.bar(x + width/2, after_values, width, label='改进后',
                       color='#66b2ff', alpha=0.8, edgecolor='black')
        
        # 添加数值标签
        for bar in bars1:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height}', ha='center', va='bottom', fontweight='bold')
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height}', ha='center', va='bottom', fontweight='bold')
        
        ax2.set_xlabel('产品类别', fontsize=12)
        ax2.set_ylabel('性能评分', fontsize=12)
        ax2.set_title('✅ 设计良好的对比图', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(categories)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_facecolor('#f8f9fa')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def color_palette_guide():
        """色彩搭配指南"""
        print("=== 推荐色彩搭配方案 ===")
        
        # 定义几种专业配色方案
        palettes = {
            '商务蓝调': ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78'],
            '清新绿色': ['#2ca02c', '#98df8a', '#d62728', '#ff9896'],
            '温暖橙红': ['#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a'],
            '专业灰调': ['#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d'],
            '活力彩虹': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        }
        
        fig, axes = plt.subplots(1, len(palettes), figsize=(20, 4))
        fig.suptitle('专业色彩搭配方案', fontsize=16, fontweight='bold')
        
        sample_data = [30, 25, 20, 15, 10]
        
        for i, (name, colors) in enumerate(palettes.items()):
            wedges, texts = axes[i].pie(sample_data, colors=colors, startangle=90)
            axes[i].set_title(name, fontsize=12, pad=10)
            axes[i].axis('equal')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def dashboard_layout_example():
        """仪表板布局示例"""
        print("=== 数据仪表板布局示例 ===")
        
        # 创建复杂的仪表板布局
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('销售数据分析仪表板', fontsize=20, fontweight='bold', y=0.95)
        
        # 使用GridSpec创建复杂布局
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 第一行：关键指标
        ax1 = fig.add_subplot(gs[0, :])
        metrics = ['总收入', '订单数量', '客户满意度', '增长率']
        values = [1250000, 1500, 4.2, 15.5]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        bars = ax1.bar(metrics, values, color=colors, alpha=0.8)
        ax1.set_title('关键业务指标', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylabel('数值')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 为每个柱子添加数值标签
        for bar, value in zip(bars, values):
            if isinstance(value, (int, float)):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'{value:,}' if value > 1000 else f'{value}',
                        ha='center', va='bottom', fontweight='bold')
        
        # 第二行左边：趋势图
        ax2 = fig.add_subplot(gs[1, :2])
        dates = pd.date_range('2023-01-01', periods=12, freq='M')
        revenue = [100000 + i*8000 + np.random.randint(-5000, 5000) for i in range(12)]
        
        ax2.plot(dates, revenue, 'b-o', linewidth=2, markersize=6)
        ax2.set_title('月度收入趋势', fontsize=12, fontweight='bold')
        ax2.set_ylabel('收入 ($)')
        ax2.grid(True, alpha=0.3)
        
        # 第二行右边：占比图
        ax3 = fig.add_subplot(gs[1, 2])
        regions = ['华东', '华南', '华北', '其他']
        region_sales = [45, 30, 20, 5]
        ax3.pie(region_sales, labels=regions, autopct='%1.1f%%', startangle=90)
        ax3.set_title('区域销售占比', fontsize=12, fontweight='bold')
        
        # 第三行：详细分析
        ax4 = fig.add_subplot(gs[2, :-1])
        products = ['产品A', '产品B', '产品C', '产品D', '产品E']
        sales_data = [120, 95, 80, 70, 60]
        ax4.barh(products, sales_data, color=plt.cm.viridis(np.linspace(0, 1, len(products))))
        ax4.set_title('产品销售排名', fontsize=12, fontweight='bold')
        ax4.set_xlabel('销售数量')
        ax4.grid(True, alpha=0.3, axis='x')
        
        # 第三行右边：数据表格效果
        ax5 = fig.add_subplot(gs[2, -1])
        ax5.axis('off')
        
        # 创建表格数据
        table_data = [
            ['指标', '数值', '变化'],
            ['新客户', '1,250', '+12%'],
            ['复购率', '68%', '+3%'],
            ['客单价', '$245', '+8%'],
            ['转化率', '3.2%', '+0.5%']
        ]
        
        table = ax5.table(cellText=table_data, cellLoc='center', loc='center',
                         colWidths=[0.4, 0.3, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # 美化表格
        for i in range(len(table_data)):
            for j in range(len(table_data[0])):
                cell = table[(i, j)]
                if i == 0:  # 表头
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax5.set_title('关键指标速览', fontsize=12, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.show()

def main():
    """演示所有工具和最佳实践"""
    print("=" * 60)
    print("Matplotlib 实用工具类和最佳实践演示")
    print("=" * 60)
    
    # 1. 模板使用示例
    print("\n--- 图表模板示例 ---")
    
    # 折线图模板
    x = np.linspace(0, 10, 50)
    y = np.sin(x) + 0.1 * np.random.randn(50)
    fig1, ax1 = PlotTemplates.clean_line_chart(
        x, y, "示例折线图", "时间", "数值", color='blue'
    )
    plt.show()
    
    # 柱状图模板
    categories = ['类别A', '类别B', '类别C', '类别D']
    values = [23, 45, 56, 32]
    fig2, ax2 = PlotTemplates.professional_bar_chart(
        categories, values, "示例柱状图", "类别", "数值"
    )
    plt.show()
    
    # 2. 工具类使用示例
    print("\n--- 工具类示例 ---")
    
    # 创建示例数据框
    np.random.seed(42)
    df = pd.DataFrame({
        '销售额': np.random.randn(100) * 1000 + 5000,
        '成本': np.random.randn(100) * 500 + 3000,
        '利润': np.random.randn(100) * 300 + 1000,
        '客户数': np.random.randint(50, 200, 100)
    })
    
    # 相关性热力图
    fig3, ax3 = DataVisualizationUtils.create_correlation_heatmap(
        df, "业务指标相关性分析"
    )
    plt.show()
    
    # 3. 最佳实践演示
    print("\n--- 最佳实践演示 ---")
    BestPracticesDemo.before_after_comparison()
    BestPracticesDemo.color_palette_guide()
    BestPracticesDemo.dashboard_layout_example()
    
    print("\n所有演示完成！")

if __name__ == "__main__":
    main()