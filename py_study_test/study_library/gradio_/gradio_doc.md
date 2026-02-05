# Gradio 核心 API 完整文档

## 📋 目录
1. [概述](#概述)
2. [核心接口](#核心接口)
3. [输入组件](#输入组件)
4. [输出组件](#输出组件)
5. [布局系统](#布局系统)
6. [事件处理](#事件处理)
7. [高级功能](#高级功能)
8. [最佳实践](#最佳实践)

## 概述

Gradio 是一个用于快速创建机器学习模型 Web 界面的 Python 库。它提供了简单易用的 API 来包装任何 Python 函数，使其可以通过 Web 界面进行交互。

### 主要优势
- 🚀 **快速开发**: 几行代码即可创建 Web 应用
- 🎨 **丰富组件**: 支持文本、图像、音频等多种数据类型
- 🔧 **灵活配置**: 可自定义样式、布局和交互行为
- ☁️ **易于部署**: 支持本地和云端部署

## 核心接口

### gr.Interface
最简单的应用创建方式，适用于单一函数的快速包装。

```python
import gradio as gr

def my_function(input_data):
    # 处理逻辑
    return output_data

interface = gr.Interface(
    fn=my_function,
    inputs=[input_component1, input_component2],
    outputs=[output_component1],
    title="应用标题",
    description="应用描述"
)

interface.launch()
```

#### 主要参数
- `fn`: 要包装的 Python 函数
- `inputs`: 输入组件列表
- `outputs`: 输出组件列表
- `title`: 应用标题
- `description`: 应用描述
- `examples`: 示例数据

### gr.Blocks
更灵活的布局构建器，支持复杂的应用结构。

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# 我的应用")
    
    with gr.Row():
        with gr.Column():
            input_component = gr.Textbox()
        with gr.Column():
            output_component = gr.Textbox()
    
    btn = gr.Button("处理")
    btn.click(my_function, inputs=input_component, outputs=output_component)

demo.launch()
```

## 输入组件

### 文本输入组件

#### Textbox
多行文本输入框
```python
textbox = gr.Textbox(
    label="输入文本",
    placeholder="请输入内容...",
    lines=3,           # 显示行数
    max_lines=5,       # 最大行数
    value="默认值"      # 默认值
)
```

#### Text
单行文本输入
```python
text_input = gr.Text(
    label="用户名",
    placeholder="请输入用户名"
)
```

#### Number
数字输入
```python
number_input = gr.Number(
    label="年龄",
    minimum=0,         # 最小值
    maximum=120,       # 最大值
    step=1,            # 步长
    value=25           # 默认值
)
```

#### Slider
滑块输入
```python
slider = gr.Slider(
    minimum=0,         # 最小值
    maximum=100,       # 最大值
    value=50,          # 默认值
    step=1,            # 步长
    label="参数调节"
)
```

### 选择组件

#### Radio
单选按钮
```python
radio = gr.Radio(
    choices=["选项1", "选项2", "选项3"],
    label="请选择",
    value="选项1"      # 默认选中项
)
```

#### Checkbox
复选框
```python
checkbox = gr.Checkbox(
    label="启用功能",
    value=False        # 默认状态
)
```

#### Dropdown
下拉选择
```python
dropdown = gr.Dropdown(
    choices=["苹果", "香蕉", "橙子"],
    label="选择水果",
    multiselect=True,  # 是否支持多选
    value="苹果"       # 默认值
)
```

#### CheckboxGroup
复选框组
```python
checkbox_group = gr.CheckboxGroup(
    choices=["红色", "绿色", "蓝色"],
    label="选择颜色",
    value=["红色"]     # 默认选中项
)
```

### 媒体组件

#### Image
图像输入
```python
image_input = gr.Image(
    label="上传图片",
    type="numpy",      # "filepath", "numpy", "pil"
    sources=["upload", "clipboard", "webcam"],  # 输入源
    shape=(224, 224)   # 指定尺寸
)
```

#### Audio
音频输入
```python
audio_input = gr.Audio(
    label="音频输入",
    type="filepath",   # "filepath", "numpy"
    sources=["upload", "microphone"]  # 输入源
)
```

#### Video
视频输入
```python
video_input = gr.Video(
    label="视频输入",
    sources=["upload", "webcam"]
)
```

### 文件和数据组件

#### File
文件上传
```python
file_input = gr.File(
    label="文件上传",
    file_types=[".txt", ".csv", ".pdf"],  # 限制文件类型
    file_count="multiple"  # "single" 或 "multiple"
)
```

#### Dataframe
数据表格
```python
dataframe = gr.Dataframe(
    label="数据表格",
    headers=["列1", "列2", "列3"],
    datatype=["str", "number", "str"],
    row_count=5,
    col_count=(3, "fixed")  # (列数, 类型)
)
```

## 输出组件

### 显示组件

#### Label
标签输出（常用于分类结果）
```python
label_output = gr.Label(
    label="分类结果",
    num_top_classes=3  # 显示前N个最高概率
)
```

#### Textbox
文本输出
```python
text_output = gr.Textbox(
    label="处理结果",
    lines=5,
    interactive=False  # 是否可编辑
)
```

#### JSON
JSON 数据输出
```python
json_output = gr.JSON(label="详细信息")
```

#### HTML
HTML 内容输出
```python
html_output = gr.HTML(label="格式化内容")
```

### 可视化组件

#### Plot
matplotlib 图表输出
```python
plot_output = gr.Plot(label="数据图表")
```

#### Image
图像输出
```python
image_output = gr.Image(label="处理后图片")
```

#### Audio
音频输出
```python
audio_output = gr.Audio(label="生成音频")
```

#### Video
视频输出
```python
video_output = gr.Video(label="处理后视频")
```

## 布局系统

### 基本布局容器

#### Row
水平排列组件
```python
with gr.Row():
    component1 = gr.Textbox()
    component2 = gr.Textbox()
```

#### Column
垂直排列组件
```python
with gr.Column():
    component1 = gr.Textbox()
    component2 = gr.Textbox()
```

#### Group
将相关组件分组
```python
with gr.Group():
    gr.Markdown("### 用户信息")
    name = gr.Textbox(label="姓名")
    email = gr.Textbox(label="邮箱")
```

### 高级布局

#### Tab
标签页布局
```python
with gr.Tab("标签1"):
    # 标签1的内容
    component1 = gr.Textbox()

with gr.Tab("标签2"):
    # 标签2的内容
    component2 = gr.Textbox()
```

#### Accordion
可折叠面板
```python
with gr.Accordion("高级设置", open=False):
    advanced_setting1 = gr.Slider()
    advanced_setting2 = gr.Checkbox()
```

## 事件处理

### 基本事件

#### click
按钮点击事件
```python
btn = gr.Button("提交")
btn.click(
    fn=process_function,
    inputs=[input1, input2],
    outputs=[output1]
)
```

#### change
组件值改变事件
```python
slider = gr.Slider()
slider.change(
    fn=update_function,
    inputs=slider,
    outputs=output
)
```

#### submit
表单提交事件（通常用于文本框回车）
```python
textbox = gr.Textbox()
textbox.submit(
    fn=process_text,
    inputs=textbox,
    outputs=output
)
```

### 事件链

#### then
顺序执行多个函数
```python
btn.click(
    fn=step1_function,
    inputs=input1,
    outputs=temp_result
).then(
    fn=step2_function,
    inputs=temp_result,
    outputs=final_result
)
```

#### success / fail
成功/失败回调
```python
btn.click(
    fn=main_function,
    inputs=inputs,
    outputs=outputs
).success(
    fn=success_callback,
    inputs=None,
    outputs=None
).fail(
    fn=failure_callback,
    inputs=None,
    outputs=None
)
```

## 高级功能

### 状态管理

#### gr.State
维护应用状态
```python
# 初始化状态
counter_state = gr.State(value=0)
history_state = gr.State(value=[])

def increment(counter):
    return counter + 1

btn.click(
    increment,
    inputs=counter_state,
    outputs=counter_state
)
```

### 条件显示

#### 动态控制可见性
```python
def toggle_visibility(checked):
    return gr.update(visible=checked)

checkbox = gr.Checkbox()
hidden_component = gr.Textbox(visible=False)

checkbox.change(
    toggle_visibility,
    inputs=checkbox,
    outputs=hidden_component
)
```

### 自定义样式

#### CSS 样式
```python
with gr.Blocks(css=".my-class { color: red; }") as demo:
    textbox = gr.Textbox(elem_classes=["my-class"])
```

#### 主题定制
```python
demo = gr.Blocks(theme=gr.themes.Soft())
```

### 性能优化

#### 批量处理
```python
def batch_process(items):
    return [process_item(item) for item in items]

interface = gr.Interface(
    fn=batch_process,
    inputs=gr.File(file_count="multiple"),
    outputs=gr.File()
)
```

#### 异步处理
```python
import asyncio

async def async_process(data):
    await asyncio.sleep(1)  # 模拟异步操作
    return process_data(data)

interface = gr.Interface(
    fn=async_process,
    inputs=gr.Textbox(),
    outputs=gr.Textbox()
)
```

## 最佳实践

### 1. 组件设计原则

#### 合理分组
```python
# ✅ 好的做法
with gr.Group():
    gr.Markdown("### 基本信息")
    name = gr.Textbox(label="姓名")
    age = gr.Number(label="年龄")

# ❌ 避免的做法
name = gr.Textbox(label="姓名")
age = gr.Number(label="年龄")
# 缺少逻辑分组
```

#### 清晰的标签
```python
# ✅ 好的做法
temperature = gr.Slider(
    label="温度设置 (°C)",
    info="调节处理温度参数"
)

# ❌ 避免的做法
temp = gr.Slider(label="Temp")  # 标签不够清晰
```

### 2. 错误处理

#### 输入验证
```python
def safe_process(text):
    if not text:
        raise ValueError("输入不能为空")
    return process_text(text)

interface = gr.Interface(
    fn=safe_process,
    inputs=gr.Textbox(),
    outputs=gr.Textbox()
)
```

#### 优雅降级
```python
def robust_function(data):
    try:
        return process_data(data)
    except Exception as e:
        return f"处理失败: {str(e)}"
```

### 3. 用户体验优化

#### 加载状态
```python
btn = gr.Button("处理")
btn.click(
    fn=long_process,
    inputs=input_data,
    outputs=output_data,
    api_name="process"  # API 端点名称
)
```

#### 进度指示
```python
def process_with_progress(data, progress=gr.Progress()):
    progress(0, desc="开始处理...")
    # 处理逻辑
    for i in range(100):
        progress(i/100, desc=f"处理进度 {i}%")
    progress(1, desc="处理完成")
    return result
```

### 4. 部署考虑

#### 服务器配置
```python
interface.launch(
    server_name="0.0.0.0",  # 允许外部访问
    server_port=7860,
    share=False,            # 不创建公共链接
    max_threads=40,         # 最大线程数
    show_api=True           # 显示 API 文档
)
```

#### 安全配置
```python
interface.launch(
    auth=("username", "password"),  # 基本身份验证
    ssl_verify=False,               # SSL 配置
    prevent_thread_lock=True        # 防止线程锁
)
```

## 常见问题解答

### Q: 如何处理大型文件？
A: 使用 `streaming=True` 参数和分块处理：

```python
def process_large_file(file_obj):
    # 分块处理大文件
    chunk_size = 1024 * 1024  # 1MB
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break
        # 处理块数据
```

### Q: 如何实现实时更新？
A: 使用 `every` 参数：

```python
component.change(
    fn=update_function,
    inputs=inputs,
    outputs=outputs,
    every=1  # 每秒更新一次
)
```

### Q: 如何自定义组件外观？
A: 使用 CSS 和 `elem_classes`：

```python
with gr.Blocks(css="""
    .custom-input { border: 2px solid blue; }
    .custom-button { background-color: green; }
"""):
    textbox = gr.Textbox(elem_classes=["custom-input"])
    button = gr.Button("提交", elem_classes=["custom-button"])
```

---

*文档版本: 1.0*  
*最后更新: 2024年*