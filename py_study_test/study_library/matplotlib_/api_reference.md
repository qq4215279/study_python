# Matplotlib & NumPy API 详细注释参考

## 📊 Matplotlib 核心API详解

### 基础绘图函数

#### `plt.figure()`
```python
plt.figure(figsize=(width, height))
```
- **功能**：创建新的图表窗口
- **参数**：
  - `figsize`：图表尺寸，单位为英寸 (宽度, 高度)
  - `dpi`：分辨率，默认100
  - `facecolor`：背景颜色

#### `plt.plot()`
```python
plt.plot(x, y, 'b-', linewidth=2, label='标签')
```
- **功能**：绘制线条图
- **参数**：
  - `x, y`：数据坐标
  - 线条样式：`'b-'`(蓝实线), `'r--'`(红虚线), `'g:'`(绿点线)
  - `linewidth`：线宽
  - `label`：图例标签
  - `marker`：标记样式 (`'o'`, `'s'`, `'^'`等)

#### `plt.scatter()`
```python
plt.scatter(x, y, c='color', alpha=0.6, s=50)
```
- **功能**：绘制散点图
- **参数**：
  - `c`：颜色
  - `alpha`：透明度 (0-1)
  - `s`：点的大小
  - `marker`：点的形状

#### `plt.bar()`
```python
plt.bar(categories, values, color=['red', 'blue', 'green'])
```
- **功能**：绘制柱状图
- **参数**：
  - `categories`：类别标签
  - `values`：对应数值
  - `color`：颜色列表
  - 返回柱子对象，可用于添加标签

#### `plt.pie()`
```python
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
```
- **功能**：绘制饼图
- **参数**：
  - `sizes`：各部分大小
  - `labels`：标签
  - `colors`：颜色
  - `autopct`：自动计算百分比格式
  - `startangle`：起始角度

#### `plt.hist()`
```python
plt.hist(data, bins=30, color='skyblue', edgecolor='black')
```
- **功能**：绘制直方图
- **参数**：
  - `data`：数据
  - `bins`：分箱数量
  - `color`：填充颜色
  - `edgecolor`：边缘颜色
  - `alpha`：透明度

#### `plt.fill_between()`
```python
plt.fill_between(x, y, alpha=0.3, color='orange')
```
- **功能**：绘制填充区域图
- **参数**：
  - `x`：x坐标
  - `y`：y坐标
  - `alpha`：透明度
  - `color`：填充颜色

### 子图和布局

#### `plt.subplot()` 和 `plt.subplots()`
```python
# subplot - 逐个创建子图
plt.subplot(2, 3, 1)  # 2行3列，第1个子图

# subplots - 一次性创建所有子图
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
```

#### `plt.tight_layout()`
```python
plt.tight_layout()
```
- **功能**：自动调整子图间距，防止重叠

### 坐标轴设置

#### 坐标轴标签
```python
plt.xlabel('X轴标签', fontsize=12, fontweight='bold')
plt.ylabel('Y轴标签', fontsize=12, fontweight='bold')
```

#### 标题设置
```python
plt.title('图表标题', fontsize=14, fontweight='bold', pad=20)
```

#### 刻度设置
```python
plt.tick_params(axis='both', which='major', labelsize=10)
plt.tick_params(axis='x', rotation=45)
```

### 网格和背景

#### 网格线
```python
plt.grid(True, linestyle='--', alpha=0.7)
```

#### 背景颜色
```python
plt.set_facecolor('#f0f0f0')
```

### 高级功能

#### 双Y轴
```python
ax2_twin = ax2.twinx()  # 创建共享x轴的第二个y轴
```

#### 极坐标图
```python
ax = plt.subplot(1, 1, 1, projection='polar')
```

#### 3D图
```python
from mpl_toolkits.mplot3d import Axes3D
ax = plt.subplot(1, 1, 1, projection='3d')
```

#### 注释和文本
```python
# 添加文本注释
plt.annotate('注释文本', xy=(x, y), xytext=(x_offset, y_offset),
            arrowprops=dict(arrowstyle='->'))

# 直接添加文本
plt.text(x, y, '文本内容', ha='center', va='bottom')
```

#### 参考线
```python
# 水平线
plt.axhline(y=value, color='red', linestyle='--')

# 垂直线  
plt.axvline(x=value, color='green', linestyle=':')
```

## 🔢 NumPy 核心API详解

### 数组创建

#### `np.linspace()`
```python
x = np.linspace(start, stop, num=50)
```
- **功能**：在指定区间内生成等间距的数组
- **参数**：
  - `start`：起始值
  - `stop`：结束值
  - `num`：生成点数

#### `np.arange()`
```python
x = np.arange(start, stop, step)
```
- **功能**：生成等步长的数组
- **参数**：
  - `start`：起始值
  - `stop`：结束值（不包含）
  - `step`：步长

### 随机数生成

#### `np.random.randn()`
```python
data = np.random.randn(size)
```
- **功能**：生成标准正态分布随机数（均值0，标准差1）
- **参数**：`size` - 生成数量

#### `np.random.normal()`
```python
data = np.random.normal(mean, std, size)
```
- **功能**：生成指定均值和标准差的正态分布随机数
- **参数**：
  - `mean`：均值
  - `std`：标准差
  - `size`：生成数量

### 数学函数

#### 三角函数
```python
y = np.sin(x)    # 正弦函数
y = np.cos(x)    # 余弦函数
y = np.tan(x)    # 正切函数
```

#### 指数和对数
```python
y = np.exp(x)     # 指数函数 e^x
y = np.log(x)     # 自然对数 ln(x)
y = np.log10(x)   # 常用对数 log10(x)
```

#### 其他函数
```python
y = np.sqrt(x)    # 平方根
y = np.abs(x)     # 绝对值
y = np.power(x, n) # x的n次幂
```

### 数组操作

#### 统计函数
```python
mean_val = np.mean(array)      # 平均值
std_val = np.std(array)        # 标准差
max_val = np.max(array)        # 最大值
min_val = np.min(array)        # 最小值
```

#### 累积运算
```python
cumsum_array = np.cumsum(array)  # 累积和
cumprod_array = np.cumprod(array) # 累积积
```

#### 索引和查找
```python
max_index = np.argmax(array)   # 最大值索引
min_index = np.argmin(array)   # 最小值索引
```

### 网格生成

#### `np.meshgrid()`
```python
X, Y = np.meshgrid(x_array, y_array)
```
- **功能**：从一维坐标向量创建二维网格坐标矩阵
- **用途**：3D绘图和等高线图的基础

## 📈 Pandas 相关API

### 日期时间处理

#### `pd.date_range()`
```python
dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
```
- **功能**：创建日期时间范围
- **参数**：
  - `start`：起始日期
  - `periods`：日期数量
  - `freq`：频率 ('D'=每日, 'B'=工作日, 'M'=月末等)

### 数据处理

#### 移动平均
```python
ma = pd.Series(data).rolling(window=20).mean()
```
- **功能**：计算移动平均
- **参数**：`window` - 窗口大小

#### 相关系数
```python
corr_matrix = np.corrcoef([array1, array2, array3])
```
- **功能**：计算多个数组间的相关系数矩阵

## 💡 使用技巧

### 1. 面向对象 vs Pyplot
```python
# Pyplot方式（简单）
plt.plot(x, y)
plt.show()

# 面向对象方式（推荐）
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

### 2. 颜色和样式
- **基本颜色**：`'b'`(蓝), `'r'`(红), `'g'`(绿), `'k'`(黑), `'w'`(白)
- **线型**：`'-'`(实线), `'--'`(虚线), `'-.'`(点划线), `':'`(点线)
- **标记**：`'o'`(圆点), `'s'`(方形), `'^'`(三角), `'*'`(星形)

### 3. 中文支持配置
```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
```

这份参考文档涵盖了代码中使用的主要API，每个函数都有详细的参数说明和使用示例，帮助您更好地理解和学习Matplotlib和NumPy的核心功能。