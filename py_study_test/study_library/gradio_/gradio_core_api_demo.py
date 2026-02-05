"""
Gradio 核心 API 详解演示
======================

本文件详细介绍了 Gradio 的核心 API 和使用方法，
包含各种组件、接口类型和高级功能的完整示例。
"""

import gradio as gr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import json
import time

print("🚀 Gradio 核心 API 演示开始")

# ==================== 1. 核心接口类型 ====================

# 1.1 Interface - 简单函数包装器
def simple_calculator(x, y, operation):
    """简单计算器函数"""
    operations = {
        "加法": lambda a, b: a + b,
        "减法": lambda a, b: a - b,
        "乘法": lambda a, b: a * b,
        "除法": lambda a, b: a / b if b != 0 else "错误：除数为零"
    }
    return operations[operation](x, y)

simple_interface = gr.Interface(
    fn=simple_calculator,
    inputs=[
        gr.Number(label="第一个数"),
        gr.Number(label="第二个数"),
        gr.Radio(["加法", "减法", "乘法", "除法"], label="运算类型")
    ],
    outputs=gr.Textbox(label="计算结果"),
    title="🔢 简单计算器",
    description="使用 Interface 快速创建计算器应用"
)

# 1.2 Blocks - 灵活的布局构建器
with gr.Blocks(title="🏗️ Blocks 高级布局") as blocks_demo:
    gr.Markdown("# Gradio Blocks 高级功能演示")
    
    with gr.Tab("📊 数据处理"):
        with gr.Row():
            with gr.Column(scale=1):
                data_input = gr.Textbox(
                    label="输入数据（逗号分隔）",
                    value="1,2,3,4,5,6,7,8,9,10"
                )
                process_btn = gr.Button("处理数据")
            
            with gr.Column(scale=2):
                stats_display = gr.JSON(label="统计信息")
                chart_display = gr.Plot(label="数据可视化")
        
        def process_data(data_str):
            numbers = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            stats = {
                "count": len(numbers),
                "mean": sum(numbers)/len(numbers),
                "min": min(numbers),
                "max": max(numbers)
            }
            
            fig, ax = plt.subplots()
            ax.hist(numbers, bins=len(numbers)//2)
            ax.set_title("数据分布")
            return stats, fig
        
        process_btn.click(process_data, data_input, [stats_display, chart_display])
    
    with gr.Tab("🔄 实时交互"):
        with gr.Row():
            slider1 = gr.Slider(0, 100, value=50, label="参数1")
            slider2 = gr.Slider(0, 100, value=30, label="参数2")
        
        result_text = gr.Textbox(label="实时计算结果")
        
        def calculate_sum(a, b):
            return f"参数1 + 参数2 = {a + b}"
        
        # 实时更新
        slider1.change(calculate_sum, [slider1, slider2], result_text)
        slider2.change(calculate_sum, [slider1, slider2], result_text)

# ==================== 2. 输入组件详解 ====================

# 2.1 文本相关组件
def text_components_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 📝 文本输入组件")
        
        with gr.Row():
            # Textbox - 多行文本输入
            textbox = gr.Textbox(
                label="多行文本框",
                placeholder="请输入多行文本...",
                lines=3,
                max_lines=5
            )
            
            # Text - 单行文本输入
            text_input = gr.Text(
                label="单行文本",
                placeholder="单行输入"
            )
        
        # Number - 数字输入
        number_input = gr.Number(
            label="数字输入",
            minimum=0,
            maximum=100,
            step=0.1
        )
        
        # Slider - 滑块
        slider = gr.Slider(
            minimum=0,
            maximum=100,
            value=50,
            step=1,
            label="滑块控件"
        )
        
        output = gr.Textbox(label="输出结果")
        
        def process_inputs(tb_val, txt_val, num_val, slide_val):
            return f"""
            文本框内容: {tb_val}
            单行文本: {txt_val}
            数字: {num_val}
            滑块值: {slide_val}
            """
        
        # 绑定所有输入到同一个函数
        for component in [textbox, text_input, number_input, slider]:
            component.change(
                process_inputs,
                [textbox, text_input, number_input, slider],
                output
            )
    
    return demo

# 2.2 选择组件
def selection_components_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 🔘 选择组件")
        
        with gr.Row():
            # Radio - 单选按钮
            radio = gr.Radio(
                choices=["选项A", "选项B", "选项C"],
                label="单选按钮",
                value="选项A"
            )
            
            # Checkbox - 复选框
            checkbox = gr.Checkbox(label="启用功能")
        
        # Dropdown - 下拉选择
        dropdown = gr.Dropdown(
            choices=["苹果", "香蕉", "橙子", "葡萄"],
            label="水果选择",
            multiselect=True  # 支持多选
        )
        
        # CheckboxGroup - 复选框组
        checkbox_group = gr.CheckboxGroup(
            choices=["红色", "绿色", "蓝色", "黄色"],
            label="颜色选择"
        )
        
        output = gr.JSON(label="选择结果")
        
        def process_selections(radio_val, checkbox_val, dropdown_val, checkbox_group_val):
            return {
                "单选结果": radio_val,
                "复选框状态": checkbox_val,
                "下拉选择": dropdown_val,
                "复选框组": checkbox_group_val
            }
        
        # 绑定所有选择组件
        for component in [radio, checkbox, dropdown, checkbox_group]:
            component.change(
                process_selections,
                [radio, checkbox, dropdown, checkbox_group],
                output
            )
    
    return demo

# 2.3 媒体组件
def media_components_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 🖼️ 媒体组件")
        
        with gr.Tab("图像处理"):
            with gr.Row():
                image_input = gr.Image(
                    label="上传图片",
                    type="numpy",  # 可选: "filepath", "numpy", "pil"
                    sources=["upload", "clipboard", "webcam"]  # 支持多种输入源
                )
                image_output = gr.Image(label="处理后图片")
            
            btn_process = gr.Button("处理图片")
            
            def process_image(img):
                if img is not None:
                    # 简单的图像处理：反转颜色
                    processed = 255 - img
                    return processed
                return None
            
            btn_process.click(process_image, image_input, image_output)
        
        with gr.Tab("音频处理"):
            audio_input = gr.Audio(
                label="音频输入",
                type="filepath",  # 可选: "filepath", "numpy"
                sources=["upload", "microphone"]
            )
            audio_output = gr.Audio(label="音频输出")
            
            def process_audio(audio):
                # 这里可以添加音频处理逻辑
                return audio  # 简单回传
            
            audio_input.change(process_audio, audio_input, audio_output)
        
        with gr.Tab("视频处理"):
            video_input = gr.Video(label="视频输入")
            video_output = gr.Video(label="视频输出")
            
            def process_video(video):
                return video  # 简单回传
            
            video_input.change(process_video, video_input, video_output)
    
    return demo

# 2.4 文件和数据组件
def file_data_components_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 📁 文件和数据组件")
        
        with gr.Row():
            # File - 文件上传
            file_input = gr.File(
                label="文件上传",
                file_types=[".txt", ".csv", ".json"],  # 限制文件类型
                file_count="multiple"  # 支持多文件
            )
            
            # Dataframe - 数据表格
            df_input = gr.Dataframe(
                label="数据表格输入",
                headers=["姓名", "年龄", "城市"],
                datatype=["str", "number", "str"],
                row_count=5,
                col_count=(3, "fixed")
            )
        
        with gr.Row():
            file_output = gr.File(label="文件输出")
            df_output = gr.Dataframe(label="数据表格输出")
        
        def process_file_and_data(files, dataframe):
            # 处理上传的文件
            processed_files = []
            if files:
                for file in files:
                    processed_files.append(file.name)
            
            # 处理数据表格
            if dataframe is not None:
                # 添加一列
                dataframe['处理时间'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return processed_files, dataframe
        
        btn_process = gr.Button("处理文件和数据")
        btn_process.click(
            process_file_and_data,
            [file_input, df_input],
            [file_output, df_output]
        )
    
    return demo

# ==================== 3. 输出组件详解 ====================

def output_components_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 📤 输出组件")
        
        input_text = gr.Textbox(label="输入文本")
        
        with gr.Row():
            # Label - 简单文本输出
            label_output = gr.Label(label="标签输出")
            
            # Textbox - 文本输出
            textbox_output = gr.Textbox(label="文本输出", lines=3)
        
        with gr.Row():
            # JSON - JSON 数据输出
            json_output = gr.JSON(label="JSON 输出")
            
            # HTML - HTML 内容输出
            html_output = gr.HTML(label="HTML 输出")
        
        def generate_outputs(text):
            # Label 输出（通常用于分类概率）
            label_data = {f"类别{i}": np.random.random() for i in range(5)}
            
            # 文本输出
            text_result = f"您输入的内容是: {text}\n处理时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            # JSON 输出
            json_data = {
                "原始输入": text,
                "字符数": len(text),
                "处理状态": "成功",
                "时间戳": time.time()
            }
            
            # HTML 输出
            html_content = f"""
            <div style="padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                <h3>处理结果</h3>
                <p><strong>输入:</strong> {text}</p>
                <p><strong>长度:</strong> {len(text)} 字符</p>
                <p><strong>时间:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            """
            
            return label_data, text_result, json_data, html_content
        
        input_text.change(
            generate_outputs,
            input_text,
            [label_output, textbox_output, json_output, html_output]
        )
    
    return demo

# ==================== 4. 高级功能 ====================

# 4.1 状态管理
def state_management_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 💾 状态管理")
        
        # 使用 gr.State 管理应用状态
        counter_state = gr.State(value=0)
        history_state = gr.State(value=[])
        
        with gr.Row():
            increment_btn = gr.Button("增加计数")
            reset_btn = gr.Button("重置计数")
        
        counter_display = gr.Number(label="当前计数", interactive=False)
        history_display = gr.JSON(label="操作历史")
        
        def increment(counter, history):
            new_counter = counter + 1
            history.append(f"增加到 {new_counter} ({time.strftime('%H:%M:%S')})")
            return new_counter, history[-10:]  # 只保留最近10条记录
        
        def reset():
            return 0, ["计数器已重置"]
        
        increment_btn.click(
            increment,
            [counter_state, history_state],
            [counter_state, history_state]
        ).then(
            lambda c, h: (c, h),
            [counter_state, history_state],
            [counter_display, history_display]
        )
        
        reset_btn.click(
            reset,
            None,
            [counter_state, history_state]
        ).then(
            lambda c, h: (c, h),
            [counter_state, history_state],
            [counter_display, history_display]
        )
    
    return demo

# 4.2 条件显示和动态更新
def conditional_display_demo():
    with gr.Blocks() as demo:
        gr.Markdown("## 🎯 条件显示和动态更新")
        
        enable_advanced = gr.Checkbox(label="启用高级功能")
        
        with gr.Group(visible=False) as advanced_options:
            gr.Markdown("### 高级设置")
            advanced_slider = gr.Slider(0, 100, value=50, label="高级参数")
            advanced_text = gr.Textbox(label="高级文本")
        
        result = gr.Textbox(label="结果")
        
        def toggle_advanced(checked):
            return gr.update(visible=checked)
        
        def process_with_advanced(checked, slider_val, text_val):
            if checked:
                return f"高级模式: 滑块={slider_val}, 文本='{text_val}'"
            else:
                return "基础模式"
        
        enable_advanced.change(
            toggle_advanced,
            enable_advanced,
            advanced_options
        )
        
        # 绑定所有相关组件
        for component in [enable_advanced, advanced_slider, advanced_text]:
            component.change(
                process_with_advanced,
                [enable_advanced, advanced_slider, advanced_text],
                result
            )
    
    return demo

# ==================== 5. 完整应用组合 ====================

def complete_app_demo():
    with gr.Blocks(title="🔧 Gradio 完整应用演示") as app:
        gr.Markdown("""
        # 🎨 Gradio 核心 API 完整演示
        
        这是一个综合演示应用，展示了 Gradio 的所有核心功能和最佳实践。
        """)
        
        with gr.Tab("🧮 计算器"):
            simple_interface.render()
        
        with gr.Tab("🏗️ 高级布局"):
            blocks_demo.render()
        
        with gr.Tab("📝 输入组件"):
            text_components_demo().render()
        
        with gr.Tab("🔘 选择组件"):
            selection_components_demo().render()
        
        with gr.Tab("🖼️ 媒体组件"):
            media_components_demo().render()
        
        with gr.Tab("📁 文件组件"):
            file_data_components_demo().render()
        
        with gr.Tab("📤 输出组件"):
            output_components_demo().render()
        
        with gr.Tab("💾 状态管理"):
            state_management_demo().render()
        
        with gr.Tab("🎯 条件显示"):
            conditional_display_demo().render()
    
    return app

# ==================== 主程序入口 ====================

if __name__ == "__main__":
    print("正在启动 Gradio 核心 API 演示应用...")
    print("功能概览:")
    print("- 🧮 简单计算器 (Interface)")
    print("- 🏗️ 高级布局 (Blocks)")
    print("- 📝 各类输入组件")
    print("- 🔘 选择组件")
    print("- 🖼️ 媒体组件")
    print("- 📁 文件和数据组件")
    print("- 📤 输出组件")
    print("- 💾 状态管理")
    print("- 🎯 条件显示")
    
    # 启动完整的演示应用
    app = complete_app_demo()
    app.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False,
        inbrowser=True,
        show_api=False  # 隐藏 API 文档
    )