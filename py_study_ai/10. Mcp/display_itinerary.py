#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上海旅游攻略网页展示工具
将JSON格式的攻略数据转换为美观的HTML表格页面
"""

import json
from pathlib import Path
from datetime import datetime


def load_itinerary(json_file: str) -> dict:
    """加载JSON攻略文件"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到文件 {json_file}")
        return None
    except json.JSONDecodeError:
        print(f"错误：JSON文件格式不正确")
        return None


def generate_html(itinerary: dict) -> str:
    """生成HTML页面"""
    
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>上海一天旅游攻略 - {date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title::before {{
            content: '';
            width: 5px;
            height: 30px;
            background: #667eea;
            border-radius: 3px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tbody tr {{
            transition: background-color 0.3s;
        }}
        
        tbody tr:hover {{
            background-color: #f5f5f5;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .time-cell {{
            font-weight: 600;
            color: #667eea;
            white-space: nowrap;
        }}
        
        .activity-cell {{
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }}
        
        .location-cell {{
            color: #666;
        }}
        
        .description-cell {{
            color: #555;
            line-height: 1.6;
        }}
        
        .tips-cell {{
            color: #888;
            font-style: italic;
            background-color: #fff9e6;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #ffc107;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .info-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .info-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .info-card ul {{
            list-style: none;
            padding: 0;
        }}
        
        .info-card li {{
            padding: 8px 0;
            color: #555;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .info-card li:last-child {{
            border-bottom: none;
        }}
        
        .info-card li::before {{
            content: '✓ ';
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .food-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .food-tag {{
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .tips-list {{
            background: #fff9e6;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #ffc107;
        }}
        
        .tips-list li {{
            margin: 10px 0;
            color: #555;
            line-height: 1.6;
        }}
        
        .tips-list li::before {{
            content: '💡 ';
            margin-right: 8px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            table {{
                font-size: 0.9em;
            }}
            
            th, td {{
                padding: 10px;
            }}
            
            .info-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗺️ 上海一天旅游攻略</h1>
            <p>日期：{date} | 城市：{city}</p>
        </div>
        
        <div class="content">
            <!-- 行程安排表格 -->
            <div class="section">
                <div class="section-title">📅 行程安排</div>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 15%;">时间</th>
                            <th style="width: 20%;">活动</th>
                            <th style="width: 15%;">地点</th>
                            <th style="width: 30%;">说明</th>
                            <th style="width: 20%;">提示</th>
                        </tr>
                    </thead>
                    <tbody>
                        {schedule_rows}
                    </tbody>
                </table>
            </div>
            
            <!-- 交通建议 -->
            <div class="section">
                <div class="section-title">🚇 交通建议</div>
                <div class="info-grid">
                    {transportation_cards}
                </div>
            </div>
            
            <!-- 美食推荐 -->
            <div class="section">
                <div class="section-title">🍜 美食推荐</div>
                <div class="info-grid">
                    {food_cards}
                </div>
            </div>
            
            <!-- 实用提示 -->
            <div class="section">
                <div class="section-title">💡 实用提示</div>
                <div class="tips-list">
                    <ul>
                        {tips_list}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # 生成行程表格行
    schedule_rows = ""
    for item in itinerary.get('schedule', []):
        schedule_rows += f"""
                        <tr>
                            <td class="time-cell">{item.get('time', '')}</td>
                            <td class="activity-cell">{item.get('activity', '')}</td>
                            <td class="location-cell">{item.get('location', '')}</td>
                            <td class="description-cell">{item.get('description', '')}</td>
                            <td class="tips-cell">{item.get('tips', '')}</td>
                        </tr>"""
    
    # 生成交通建议卡片
    transportation_cards = ""
    for key, value in itinerary.get('transportation', {}).items():
        transportation_cards += f"""
                    <div class="info-card">
                        <h3>{key}</h3>
                        <p>{value}</p>
                    </div>"""
    
    # 生成美食推荐卡片
    food_cards = ""
    for meal_type, foods in itinerary.get('food_recommendations', {}).items():
        food_tags = "".join([f'<span class="food-tag">{food}</span>' for food in foods])
        food_cards += f"""
                    <div class="info-card">
                        <h3>{meal_type}</h3>
                        <div class="food-list">
                            {food_tags}
                        </div>
                    </div>"""
    
    # 生成提示列表
    tips_list = ""
    for tip in itinerary.get('tips', []):
        tips_list += f"<li>{tip}</li>"
    
    # 填充模板
    html = html_template.format(
        date=itinerary.get('date', ''),
        city=itinerary.get('city', ''),
        schedule_rows=schedule_rows,
        transportation_cards=transportation_cards,
        food_cards=food_cards,
        tips_list=tips_list
    )
    
    return html


def save_html(html: str, output_file: str = "shanghai_itinerary.html"):
    """保存HTML文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ HTML文件已生成：{output_file}")
        return True
    except Exception as e:
        print(f"错误：保存HTML文件失败 - {e}")
        return False


def open_in_browser(html_file: str):
    """在浏览器中打开HTML文件"""
    import webbrowser
    import os
    
    file_path = os.path.abspath(html_file)
    if os.path.exists(file_path):
        webbrowser.open(f'file://{file_path}')
        print(f"✓ 已在浏览器中打开：{html_file}")
    else:
        print(f"错误：文件不存在 {html_file}")


def main():
    """主函数"""
    json_file = "shanghai_itinerary.json"
    html_file = "shanghai_itinerary.html"
    
    print("="*60)
    print("上海旅游攻略网页生成器")
    print("="*60)
    print()
    
    # 加载JSON数据
    print(f"正在加载 {json_file}...")
    itinerary = load_itinerary(json_file)
    
    if not itinerary:
        return
    
    print(f"✓ 成功加载攻略数据")
    print(f"  日期：{itinerary.get('date', '')}")
    print(f"  城市：{itinerary.get('city', '')}")
    print(f"  行程数：{len(itinerary.get('schedule', []))}")
    print()
    
    # 生成HTML
    print("正在生成HTML页面...")
    html = generate_html(itinerary)
    
    # 保存HTML文件
    if save_html(html, html_file):
        print()
        print("="*60)
        print("生成完成！")
        print("="*60)
        print(f"HTML文件：{html_file}")
        print()
        
        # 询问是否在浏览器中打开
        try:
            response = input("是否在浏览器中打开？(y/n): ").strip().lower()
            if response == 'y' or response == 'yes' or response == '':
                open_in_browser(html_file)
        except KeyboardInterrupt:
            print("\n已取消")


if __name__ == "__main__":
    main()
