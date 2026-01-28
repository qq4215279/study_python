# 上海一天旅游攻略生成器

使用高德地图API生成上海一天旅游攻略的Python工具。

## 功能特点

- 🔍 自动搜索上海热门旅游景点
- 📍 获取景点详细信息（地址、评分、位置等）
- 🗺️ 路径规划（驾车、公交）
- 📅 生成优化的一天行程安排
- 💾 导出JSON格式的攻略文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 申请高德地图API Key

1. 访问 [高德开放平台](https://lbs.amap.com/api/webservice/summary)
2. 注册账号并登录
3. 创建应用，选择"Web服务"类型
4. 获取API Key

### 2. 配置API Key

编辑 `shanghai_travel_guide.py` 文件，将 `API_KEY` 替换为你的API Key：

```python
API_KEY = "你的API Key"
```

### 3. 运行脚本

```bash
python shanghai_travel_guide.py
```

## 输出说明

脚本会生成：
- 控制台输出的详细攻略
- `shanghai_itinerary.json` JSON格式的攻略文件

## 网页展示工具

### 使用 display_itinerary.py 生成网页表格

`display_itinerary.py` 可以将JSON格式的攻略转换为美观的HTML网页表格展示。

#### 使用方法

```bash
python display_itinerary.py
```

#### 功能特点

- 📊 美观的表格展示行程安排
- 🎨 现代化的响应式设计
- 📱 支持移动端浏览
- 🚇 展示交通建议
- 🍜 展示美食推荐
- 💡 展示实用提示

#### 输出文件

运行后会生成 `shanghai_itinerary.html` 文件，可以直接在浏览器中打开查看。

## 行程安排

默认行程包括：
- 08:30-09:30 早餐 + 外滩晨景
- 09:30-11:00 外滩漫步 + 南京路步行街
- 11:00-12:30 豫园 + 城隍庙
- 12:30-13:30 前往陆家嘴
- 13:30-15:30 东方明珠 / 上海中心大厦
- 15:30-17:00 世纪公园（可选）
- 17:00-18:30 晚餐
- 18:30-20:00 黄浦江夜游 / 外滩夜景
- 20:00-21:00 新天地夜生活

## API说明

### AmapTravelGuide 类

主要方法：
- `search_poi()`: 搜索POI（兴趣点）
- `get_route()`: 获取驾车路径规划
- `get_transit_route()`: 获取公交路径规划
- `get_shanghai_attractions()`: 获取上海热门景点
- `generate_one_day_itinerary()`: 生成一天旅游攻略
- `print_itinerary()`: 打印攻略
- `save_itinerary_json()`: 保存攻略为JSON文件

## 注意事项

1. 高德地图API有调用次数限制，请合理使用
2. 部分功能需要申请相应的API权限
3. 建议提前预订热门景点门票
4. 注意天气变化，合理安排行程

## 许可证

MIT License
