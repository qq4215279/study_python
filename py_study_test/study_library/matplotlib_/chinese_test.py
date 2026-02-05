# -*- coding: utf-8 -*-
"""
中文显示测试文件
用于验证matplotlib的中文支持是否正常工作
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def test_chinese_display():
    """测试中文显示功能"""
    print("开始测试中文显示...")
    
    # 创建测试数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 第一个子图 - 基础中文标签
    ax1.plot(x, y1, 'b-', linewidth=2, label='正弦函数')
    ax1.plot(x, y2, 'r--', linewidth=2, label='余弦函数')
    ax1.set_xlabel('横轴标签')
    ax1.set_ylabel('纵轴标签')
    ax1.set_title('三角函数图像')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 第二个子图 - 更复杂的中文文本
    categories = ['第一季度', '第二季度', '第三季度', '第四季度']
    values = [23, 45, 56, 32]
    bars = ax2.bar(categories, values, color=['red', 'blue', 'green', 'orange'])
    ax2.set_xlabel('季度分类')
    ax2.set_ylabel('销售数值')
    ax2.set_title('季度销售数据对比')
    
    # 为柱状图添加中文数值标签
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}万', ha='center', va='bottom', fontweight='bold')
    
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("中文显示测试完成！如果图表中的中文正常显示，则配置成功。")

def test_special_characters():
    """测试特殊中文字符显示"""
    print("测试特殊中文字符...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 测试各种中文字符
    test_strings = [
        '中文测试：数据可视化',
        '数学符号：α β γ δ',
        '标点符号：，。！？；：""''（）',
        '数字混合：2023年 第1季度',
        '货币单位：￥$€元'
    ]
    
    y_positions = range(len(test_strings), 0, -1)
    
    for y, text in zip(y_positions, test_strings):
        ax.text(0.1, y, text, fontsize=12, verticalalignment='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(test_strings) + 1)
    ax.set_title('中文字符兼容性测试', fontsize=14, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("特殊字符测试完成！")

if __name__ == "__main__":
    print("=" * 50)
    print("Matplotlib 中文显示测试")
    print("=" * 50)
    
    test_chinese_display()
    test_special_characters()
    
    print("\n所有测试完成！")
    print("如果中文显示正常，说明配置成功。")
    print("如仍有问题，请检查系统是否安装了相应的中文字体。")