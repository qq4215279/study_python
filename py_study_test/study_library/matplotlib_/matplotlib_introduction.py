# -*- coding: utf-8 -*-
"""
Matplotlib 库详细介绍与核心API示例

Matplotlib 是 Python 中最流行的数据可视化库，用于创建静态、动态和交互式的图表。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ==================== Matplotlib 核心概念 ====================

def matplotlib_basics():
    """
    Matplotlib 基础概念介绍
    """
    print("=== Matplotlib 核心概念 ===")
    print("1. Figure: 整个图表窗口，可以包含多个子图")
    print("2. Axes: 图表中的单个绘图区域（注意：不是axis）")
    print("3. Axis: 坐标轴对象")
    print("4. Artist: 所有可见元素都是Artist对象")
    print()

def pyplot_vs_object_oriented():
    """
    两种主要的绘图方式对比
    """
    print("=== 绘图方式对比 ===")
    
    # Pyplot 方式（类似MATLAB风格）
    # plt.figure() - 创建新的图表窗口，figsize参数设置图表尺寸(宽度,高度)英寸
    plt.figure(figsize=(10, 4))
    # plt.subplot() - 创建子图网格，参数为(行数, 列数, 当前子图索引)
    plt.subplot(1, 2, 1)
    # np.linspace() - numpy函数，在指定区间内生成等间距的数值数组
    # 参数：起始值, 结束值, 生成点数
    x = np.linspace(0, 10, 100)
    # np.sin() - numpy函数，计算数组中每个元素的正弦值
    y = np.sin(x)
    # plt.plot() - 绘制线条图，参数：x数据, y数据, 线条样式, 标签
    # 'b-'表示蓝色实线，label用于图例显示
    plt.plot(x, y, 'b-', label='sin(x)')
    # plt.title() - 设置图表标题
    plt.title('Pyplot方式')
    # plt.legend() - 显示图例（基于plot中的label参数）
    plt.legend()
    
    # 面向对象方式（推荐）
    # plt.subplots() - 同时创建图表(Figure)和坐标轴(Axes)对象
    # 返回fig(图表对象)和ax(坐标轴对象数组)，参数含义同subplot
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    # ax[1] - 访问第二个子图(索引从0开始)
    # plot()方法 - Axes对象的绘图方法，用法与plt.plot相同
    ax[1].plot(x, y, 'r-', label='sin(x)')  # 'r-'表示红色实线
    # set_title()方法 - 设置该子图的标题
    ax[1].set_title('面向对象方式')
    # legend()方法 - 在该子图上显示图例
    ax[1].legend()
    
    plt.tight_layout()
    plt.show()

# ==================== 核心API详解 ====================

class MatplotlibCoreAPI:
    """Matplotlib 核心API详解"""
    
    @staticmethod
    def basic_plotting():
        """基础绘图API"""
        print("=== 基础绘图API ===")
        
        # 创建数据
        # np.linspace() - 生成0到2π之间100个等间距点
        # 2*np.pi 表示2倍圆周率，约等于6.28
        x = np.linspace(0, 2*np.pi, 100)
        # np.sin() - 计算正弦值
        y1 = np.sin(x)
        # np.cos() - 计算余弦值
        y2 = np.cos(x)
        
        # 方法1: 使用 pyplot
        # plt.figure() - 创建新的图表，设置尺寸为12x8英寸
        plt.figure(figsize=(12, 8))
        
        # plt.subplot() - 创建2行3列的子图网格，激活第1个子图(左上角)
        plt.subplot(2, 3, 1)
        # plt.plot() - 绘制第一条线：蓝色实线，线宽2，标签'sin(x)'
        plt.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
        # plt.plot() - 绘制第二条线：红色虚线，线宽2，标签'cos(x)'
        plt.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
        # plt.xlabel() - 设置x轴标签
        plt.xlabel('X轴')
        # plt.ylabel() - 设置y轴标签
        plt.ylabel('Y轴')
        # plt.title() - 设置子图标题
        plt.title('基础线条图')
        # plt.legend() - 显示图例
        plt.legend()
        # plt.grid() - 显示网格线，True表示启用
        plt.grid(True)
        
        # 散点图
        # 激活第2个子图(第一行第二列)
        plt.subplot(2, 3, 2)
        # np.random.randn() - 生成50个标准正态分布的随机数(均值0，标准差1)
        x_scatter = np.random.randn(50)
        # 生成y轴的随机数据
        y_scatter = np.random.randn(50)
        # plt.scatter() - 绘制散点图
        # 参数：x坐标, y坐标, c=颜色, alpha=透明度(0-1), s=点的大小
        plt.scatter(x_scatter, y_scatter, c='green', alpha=0.6, s=50)
        plt.xlabel('X值')
        plt.ylabel('Y值')
        plt.title('散点图')
        plt.grid(True)
        
        # 柱状图
        # 激活第3个子图(第一行第三列)
        plt.subplot(2, 3, 3)
        # 定义类别标签
        categories = ['A', 'B', 'C', 'D', 'E']
        # 对应的数值
        values = [23, 45, 56, 78, 32]
        # plt.bar() - 绘制柱状图
        # 参数：类别标签, 对应数值, color=每根柱子的颜色列表
        # 返回bars对象，可用于后续操作(如添加数值标签)
        bars = plt.bar(categories, values, color=['red', 'blue', 'green', 'orange', 'purple'])
        plt.xlabel('类别')
        plt.ylabel('数值')
        plt.title('柱状图')
        
        # 为柱状图添加数值标签
        # 遍历每个柱子对象
        for bar in bars:
            # bar.get_height() - 获取柱子的高度(数值)
            height = bar.get_height()
            # plt.text() - 在指定位置添加文本
            # 参数：x坐标, y坐标, 文本内容, ha=水平对齐, va=垂直对齐
            # bar.get_x() + bar.get_width()/2. - 计算柱子中心x坐标
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}', ha='center', va='bottom')
        
        # 饼图
        # 激活第4个子图(第二行第一列)
        plt.subplot(2, 3, 4)
        # 各部分的大小
        sizes = [15, 30, 45, 10]
        # 各部分的标签
        labels = ['类别1', '类别2', '类别3', '类别4']
        # 各部分的颜色
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        # plt.pie() - 绘制饼图
        # 参数：各部分大小, labels=标签, colors=颜色, autopct=自动计算百分比格式
        # startangle=起始角度(90表示从y轴正方向开始)
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        # plt.axis('equal') - 设置坐标轴比例相等，确保饼图为正圆形
        plt.axis('equal')
        plt.title('饼图')
        
        # 直方图
        # 激活第5个子图(第二行第二列)
        plt.subplot(2, 3, 5)
        # np.random.normal() - 生成1000个正态分布随机数
        # 参数：均值=0, 标准差=1, 生成数量=1000
        data = np.random.normal(0, 1, 1000)
        # plt.hist() - 绘制直方图
        # 参数：数据, bins=分箱数量, color=颜色, edgecolor=边缘颜色, alpha=透明度
        plt.hist(data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        plt.xlabel('数值')
        plt.ylabel('频次')
        plt.title('直方图')
        # plt.grid() - 显示网格线，alpha=0.3设置透明度
        plt.grid(True, alpha=0.3)
        
        # 填充图
        # 激活第6个子图(第二行第三列)
        plt.subplot(2, 3, 6)
        # 生成x轴数据：0到4π的100个点
        x_fill = np.linspace(0, 4*np.pi, 100)
        # 生成y轴数据：指数衰减的正弦波
        y_fill = np.exp(-x_fill/8) * np.sin(x_fill)
        # plt.fill_between() - 绘制填充区域图
        # 参数：x坐标, y坐标, alpha=透明度, color=填充颜色
        plt.fill_between(x_fill, y_fill, alpha=0.3, color='orange')
        # 再绘制一条橙色线条轮廓
        plt.plot(x_fill, y_fill, 'orange', linewidth=2)
        plt.xlabel('X轴')
        plt.ylabel('Y轴')
        plt.title('填充图')
        plt.grid(True)
        
        # plt.tight_layout() - 自动调整子图间距，防止重叠
        plt.tight_layout()
        # plt.show() - 显示图表
        plt.show()
    
    @staticmethod
    def advanced_plotting():
        """高级绘图技术"""
        print("=== 高级绘图技术 ===")
        
        # plt.subplots() - 创建2行2列的子图布局，返回fig和axes数组
        # figsize=(12, 10) - 设置图表尺寸为12x10英寸
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. 子图布局和共享坐标轴
        # 生成0到10之间的100个等间距点
        x = np.linspace(0, 10, 100)
        # 计算正弦和余弦值
        y1 = np.sin(x)
        y2 = np.cos(x)
        
        # 在第一个子图(ax1)中绘制两条曲线
        # plot() - 绘制蓝色实线，标签为'sin(x)'
        ax1.plot(x, y1, 'b-', label='sin(x)')
        # plot() - 绘制红色虚线，标签为'cos(x)'
        ax1.plot(x, y2, 'r--', label='cos(x)')
        # set_xlabel() - 设置x轴标签
        ax1.set_xlabel('X轴')
        # set_ylabel() - 设置y轴标签
        ax1.set_ylabel('Y轴')
        # set_title() - 设置子图标题
        ax1.set_title('共享坐标轴示例')
        # legend() - 显示图例
        ax1.legend()
        # grid() - 显示网格线
        ax1.grid(True)
        
        # 2. 双Y轴图
        # ax2.twinx() - 在同一x轴上创建第二个y轴(右侧)
        ax2_twin = ax2.twinx()
        # 生成0到10之间的50个点
        x2 = np.linspace(0, 10, 50)
        # 指数衰减的正弦波：exp(-x/3) * sin(2x)
        y2_1 = np.exp(-x2/3) * np.sin(2*x2)
        # 指数衰减的余弦波：exp(-x/5) * cos(2x)
        y2_2 = np.exp(-x2/5) * np.cos(2*x2)
        
        # 在左侧y轴绘制第一条曲线，返回line1对象
        line1 = ax2.plot(x2, y2_1, 'b-', linewidth=2, label='指数衰减正弦')
        # 在右侧y轴绘制第二条曲线，返回line2对象
        line2 = ax2_twin.plot(x2, y2_2, 'r--', linewidth=2, label='指数衰减余弦')
        
        # 设置坐标轴标签和标题
        ax2.set_xlabel('时间')
        ax2.set_ylabel('幅度1', color='b')  # 左侧y轴标签，蓝色
        ax2_twin.set_ylabel('幅度2', color='r')  # 右侧y轴标签，红色
        ax2.set_title('双Y轴图')
        
        # 合并图例
        # line1 + line2 - 合并两个线条对象列表
        lines = line1 + line2
        # 获取每个线条的标签
        labels = [l.get_label() for l in lines]
        # 在右上角显示合并后的图例
        ax2.legend(lines, labels, loc='upper right')
        
        # 3. 极坐标图
        # 生成0到2π之间的100个点
        theta = np.linspace(0, 2*np.pi, 100)
        # 极径：1 + 0.5*sin(5θ) - 创建花瓣形状
        r = 1 + 0.5 * np.sin(5*theta)
        
        # plt.subplot() - 创建极坐标子图
        # 参数：行, 列, 索引, projection='polar'表示极坐标投影
        ax3 = plt.subplot(2, 2, 3, projection='polar')
        # plot() - 在极坐标系中绘制曲线
        ax3.plot(theta, r, 'b-', linewidth=2)
        ax3.set_title('极坐标图')
        # grid() - 显示极坐标网格
        ax3.grid(True)
        
        # 4. 3D图
        # 导入3D绘图工具包
        from mpl_toolkits.mplot3d import Axes3D
        
        # plt.subplot() - 创建3D子图
        # projection='3d'表示三维坐标系
        ax4 = plt.subplot(2, 2, 4, projection='3d')
        # 生成-5到5之间的50个点
        x_3d = np.linspace(-5, 5, 50)
        y_3d = np.linspace(-5, 5, 50)
        # np.meshgrid() - 创建二维网格坐标矩阵
        X, Y = np.meshgrid(x_3d, y_3d)
        # 计算Z坐标：sin(sqrt(X²+Y²)) - 创建波浪形状
        Z = np.sin(np.sqrt(X**2 + Y**2))
        
        # plot_surface() - 绘制3D表面图
        # 参数：X坐标矩阵, Y坐标矩阵, Z坐标矩阵
        # cmap='viridis' - 使用viridis颜色映射
        # alpha=0.8 - 设置透明度
        surf = ax4.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        # 设置三个坐标轴的标签
        ax4.set_xlabel('X轴')
        ax4.set_ylabel('Y轴')
        ax4.set_zlabel('Z轴')
        ax4.set_title('3D表面图')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def customization_options():
        """图表自定义选项"""
        print("=== 图表自定义选项 ===")
        
        # 创建示例数据
        # pd.date_range() - pandas函数，创建日期范围
        # 参数：起始日期, periods=天数, freq='D'=每日频率
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        # np.cumsum() - numpy函数，计算累积和(模拟股价走势)
        # np.random.randn(30) - 生成30个正态分布随机数作为每日收益率
        values = np.cumsum(np.random.randn(30)) + 100
        
        # plt.subplots() - 创建单个子图
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 线条样式和标记
        # plot() - 绘制线条图，包含丰富的自定义参数
        line = ax.plot(dates, values, 
                      linestyle='-',      # linstyle: 线型 '-'实线 '--'虚线 '-.'点划线 ':'点线
                      linewidth=2,        # linewidth: 线宽
                      marker='o',         # marker: 标记样式 'o'圆点 's'方形 '^'三角形
                      markersize=6,       # markersize: 标记大小
                      markerfacecolor='red',    # markerfacecolor: 标记填充色
                      markeredgecolor='black',  # markeredgecolor: 标记边框色
                      markeredgewidth=1,        # markeredgewidth: 标记边框宽度
                      color='blue',
                      label='股票价格')
        
        # 坐标轴设置
        # set_xlabel() - 设置x轴标签，包含字体属性
        ax.set_xlabel('日期', fontsize=12, fontweight='bold')  # fontsize: 字体大小, fontweight: 字体粗细
        ax.set_ylabel('价格 ($)', fontsize=12, fontweight='bold')
        # set_title() - 设置图表标题，pad=20表示标题与图表的距离
        ax.set_title('股价走势图', fontsize=14, fontweight='bold', pad=20)
        
        # 刻度设置
        # tick_params() - 设置刻度参数
        # axis='both': 同时设置x和y轴, which='major': 主刻度
        # labelsize=10: 刻度标签字体大小
        ax.tick_params(axis='both', which='major', labelsize=10)
        # rotation=45: x轴刻度标签旋转45度
        ax.tick_params(axis='x', rotation=45)
        
        # 网格设置
        # grid() - 显示网格线
        # linestyle='--': 网格线型为虚线, alpha=0.7: 透明度
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 背景设置
        # set_facecolor() - 设置图表背景颜色
        ax.set_facecolor('#f0f0f0')  # 浅灰色背景
        
        # 添加文本注释
        # np.argmax() - numpy函数，找到数组中最大值的索引
        max_idx = np.argmax(values)
        # annotate() - 添加注释箭头
        # xy=: 注释点坐标, xytext=: 文本位置, textcoords=: 文本坐标系
        # bbox=: 文本框样式, arrowprops=: 箭头样式
        ax.annotate(f'最高点: ${values[max_idx]:.2f}', 
                   xy=(dates[max_idx], values[max_idx]),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # 添加水平线和垂直线
        # axhline() - 添加水平线
        # y=: y坐标, color=: 颜色, linestyle=: 线型, linewidth=: 线宽
        ax.axhline(y=np.mean(values), color='red', linestyle='--', 
                  linewidth=1, label=f'平均值: ${np.mean(values):.2f}')
        # axvline() - 添加垂直线
        ax.axvline(x=dates[15], color='green', linestyle=':', linewidth=1)
        
        # 图例设置
        # legend() - 显示图例
        # loc='best': 自动选择最佳位置, frameon=True: 显示图例边框
        # fancybox=True: 圆角边框, shadow=True: 添加阴影
        ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
        
        # 设置坐标轴范围
        # set_xlim() - 设置x轴显示范围
        ax.set_xlim(dates[0], dates[-1])
        # set_ylim() - 设置y轴显示范围，留出5%的边距
        ax.set_ylim(min(values)*0.95, max(values)*1.05)
        
        # plt.tight_layout() - 自动调整布局间距
        plt.tight_layout()
        # plt.show() - 显示最终图表
        plt.show()

# ==================== 实际应用示例 ====================

class PracticalExamples:
    """实际应用场景示例"""
    
    @staticmethod
    def financial_analysis():
        """金融数据分析示例"""
        print("=== 金融数据分析示例 ===")
        
        # 模拟股票数据
        np.random.seed(42)
        days = 252  # 一年交易日
        dates = pd.date_range('2023-01-01', periods=days, freq='B')
        
        # 生成随机游走价格
        returns = np.random.normal(0.001, 0.02, days)
        price = 100 * np.exp(np.cumsum(returns))
        
        # 计算技术指标
        ma_20 = pd.Series(price).rolling(window=20).mean()
        ma_50 = pd.Series(price).rolling(window=50).mean()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # 价格图
        ax1.plot(dates, price, 'b-', linewidth=1, label='股价')
        ax1.plot(dates, ma_20, 'r--', linewidth=1, label='20日均线')
        ax1.plot(dates, ma_50, 'g--', linewidth=1, label='50日均线')
        ax1.set_ylabel('价格 ($)')
        ax1.set_title('股价走势与移动平均线')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 成交量图（这里用价格波动模拟）
        volume = np.abs(returns) * 1000000
        ax2.bar(dates, volume, width=1, alpha=0.7, color='orange')
        ax2.set_ylabel('成交量')
        ax2.set_xlabel('日期')
        ax2.set_title('交易量')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def scientific_data_visualization():
        """科学数据可视化示例"""
        print("=== 科学数据可视化示例 ===")
        
        # 创建科学数据
        x = np.linspace(-10, 10, 1000)
        gaussian = np.exp(-x**2/2) / np.sqrt(2*np.pi)
        sine_wave = np.sin(2*x) * np.exp(-0.1*np.abs(x))
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. 高斯分布
        ax1.plot(x, gaussian, 'b-', linewidth=2)
        ax1.fill_between(x, gaussian, alpha=0.3, color='blue')
        ax1.set_xlabel('x')
        ax1.set_ylabel('概率密度')
        ax1.set_title('标准正态分布')
        ax1.grid(True, alpha=0.3)
        
        # 2. 阻尼振荡
        ax2.plot(x, sine_wave, 'r-', linewidth=2)
        ax2.set_xlabel('时间')
        ax2.set_ylabel('振幅')
        ax2.set_title('阻尼正弦波')
        ax2.grid(True, alpha=0.3)
        
        # 3. 对数坐标
        exponential_data = np.exp(x/5)
        ax3.semilogy(x[x > -5], exponential_data[x > -5], 'g-', linewidth=2)
        ax3.set_xlabel('x')
        ax3.set_ylabel('log(y)')
        ax3.set_title('半对数坐标图')
        ax3.grid(True, alpha=0.3)
        
        # 4. 误差棒图
        x_error = np.linspace(0, 10, 20)
        y_error = np.exp(-x_error/3) + np.random.normal(0, 0.05, 20)
        y_err = np.random.uniform(0.02, 0.08, 20)
        
        ax4.errorbar(x_error, y_error, yerr=y_err, fmt='o', capsize=5, 
                    capthick=2, elinewidth=2, markersize=6)
        ax4.set_xlabel('测量点')
        ax4.set_ylabel('测量值')
        ax4.set_title('带误差棒的数据')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def statistical_analysis():
        """统计分析图表示例"""
        print("=== 统计分析图表示例 ===")
        
        # 生成多组数据进行比较
        np.random.seed(123)
        group_a = np.random.normal(100, 15, 100)
        group_b = np.random.normal(105, 12, 100)
        group_c = np.random.normal(95, 18, 100)
        
        data = [group_a, group_b, group_c]
        labels = ['组A', '组B', '组C']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. 箱线图
        box_plot = ax1.boxplot(data, labels=labels, patch_artist=True)
        colors = ['lightblue', 'lightgreen', 'lightcoral']
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
        ax1.set_ylabel('数值')
        ax1.set_title('箱线图比较')
        ax1.grid(True, alpha=0.3)
        
        # 2. 小提琴图
        violin_parts = ax2.violinplot(data, positions=range(1, 4), showmeans=True)
        for pc, color in zip(violin_parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        ax2.set_xticks([1, 2, 3])
        ax2.set_xticklabels(labels)
        ax2.set_ylabel('数值')
        ax2.set_title('小提琴图')
        ax2.grid(True, alpha=0.3)
        
        # 3. Q-Q图（正态性检验）
        from scipy import stats
        stats.probplot(group_a, dist="norm", plot=ax3)
        ax3.set_title('Q-Q图 (组A正态性检验)')
        ax3.grid(True, alpha=0.3)
        
        # 4. 相关性热力图
        correlation_data = np.corrcoef([group_a, group_b, group_c])
        im = ax4.imshow(correlation_data, cmap='RdBu_r', vmin=-1, vmax=1)
        ax4.set_xticks([0, 1, 2])
        ax4.set_yticks([0, 1, 2])
        ax4.set_xticklabels(labels)
        ax4.set_yticklabels(labels)
        ax4.set_title('相关系数矩阵')
        
        # 添加数值标注
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax4.text(j, i, f'{correlation_data[i, j]:.2f}',
                              ha="center", va="center", color="black")
        
        plt.colorbar(im, ax=ax4)
        plt.tight_layout()
        plt.show()

# ==================== 主函数 ====================

def main():
    """主函数 - 运行所有示例"""
    print("=" * 50)
    print("Matplotlib 库详细介绍与实战示例")
    print("=" * 50)
    
    # 1. 基础概念介绍
    matplotlib_basics()
    
    # 2. 核心API演示
    print("\n开始运行核心API示例...")
    api_demo = MatplotlibCoreAPI()
    api_demo.basic_plotting()
    api_demo.advanced_plotting()
    api_demo.customization_options()
    
    # 3. 实际应用示例
    print("\n开始运行实际应用示例...")
    practical = PracticalExamples()
    practical.financial_analysis()
    practical.scientific_data_visualization()
    practical.statistical_analysis()
    
    print("\n所有示例运行完成！")

if __name__ == "__main__":
    main()