#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上海一天旅游攻略生成器
使用高德地图API获取景点信息和路线规划
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class AmapTravelGuide:
    """高德地图旅游攻略生成器"""
    
    def __init__(self, api_key: str):
        """
        初始化高德地图API客户端
        
        Args:
            api_key: 高德地图API Key
        """
        self.api_key = api_key
        self.base_url = "https://restapi.amap.com/v3"
        
    def search_poi(self, keywords: str, city: str = "上海", types: str = None) -> List[Dict]:
        """
        搜索POI（兴趣点）
        
        Args:
            keywords: 搜索关键词
            city: 城市名称
            types: POI类型（可选）
            
        Returns:
            POI列表
        """
        url = f"{self.base_url}/place/text"
        params = {
            "key": self.api_key,
            "keywords": keywords,
            "city": city,
            "output": "json",
            "offset": 20,
            "page": 1,
            "extensions": "all"
        }
        
        if types:
            params["types"] = types
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1" and data.get("pois"):
                return data["pois"]
            else:
                print(f"搜索失败: {data.get('info', '未知错误')}")
                return []
        except Exception as e:
            print(f"请求出错: {e}")
            return []
    
    def get_route(self, origin: str, destination: str, waypoints: List[str] = None) -> Optional[Dict]:
        """
        获取路径规划
        
        Args:
            origin: 起点坐标（格式：经度,纬度）
            destination: 终点坐标（格式：经度,纬度）
            waypoints: 途经点列表（可选）
            
        Returns:
            路径规划结果
        """
        url = f"{self.base_url}/direction/driving"
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "output": "json",
            "extensions": "all"
        }
        
        if waypoints:
            params["waypoints"] = "|".join(waypoints)
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                return data.get("route", {})
            else:
                print(f"路径规划失败: {data.get('info', '未知错误')}")
                return None
        except Exception as e:
            print(f"请求出错: {e}")
            return None
    
    def get_transit_route(self, origin: str, destination: str, city: str = "上海") -> Optional[Dict]:
        """
        获取公交路径规划
        
        Args:
            origin: 起点坐标（格式：经度,纬度）
            destination: 终点坐标（格式：经度,纬度）
            city: 城市名称
            
        Returns:
            公交路径规划结果
        """
        url = f"{self.base_url}/direction/transit/integrated"
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "city": city,
            "output": "json",
            "extensions": "all"
        }
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                return data.get("route", {})
            else:
                print(f"公交路径规划失败: {data.get('info', '未知错误')}")
                return None
        except Exception as e:
            print(f"请求出错: {e}")
            return None
    
    def get_shanghai_attractions(self) -> List[Dict]:
        """获取上海热门景点列表"""
        attractions = []
        
        # 定义上海热门景点关键词
        keywords_list = [
            "外滩",
            "东方明珠",
            "豫园",
            "城隍庙",
            "南京路步行街",
            "上海中心大厦",
            "田子坊",
            "新天地",
            "朱家角古镇",
            "上海博物馆",
            "陆家嘴",
            "世纪公园"
        ]
        
        print("正在搜索上海热门景点...")
        for keyword in keywords_list:
            pois = self.search_poi(keyword, city="上海", types="110000")  # 110000表示风景名胜
            if pois:
                # 取第一个结果
                poi = pois[0]
                attractions.append({
                    "name": poi.get("name", ""),
                    "address": poi.get("address", ""),
                    "location": poi.get("location", ""),  # 经度,纬度
                    "tel": poi.get("tel", ""),
                    "type": poi.get("type", ""),
                    "rating": poi.get("biz_ext", {}).get("rating", ""),
                    "cost": poi.get("biz_ext", {}).get("cost", ""),
                })
                print(f"✓ 找到: {poi.get('name', '')}")
        
        return attractions
    
    def generate_one_day_itinerary(self) -> Dict:
        """生成上海一天旅游攻略"""
        print("\n" + "="*60)
        print("正在生成上海一天旅游攻略...")
        print("="*60 + "\n")
        
        # 获取景点信息
        attractions = self.get_shanghai_attractions()
        
        # 定义一天的行程安排（按地理位置和游览时间优化）
        itinerary = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "city": "上海",
            "schedule": [
                {
                    "time": "08:30-09:30",
                    "activity": "早餐 + 外滩晨景",
                    "location": "外滩",
                    "description": "品尝上海特色早餐（生煎包、小笼包），欣赏黄浦江晨景和万国建筑博览群",
                    "attraction": self._find_attraction(attractions, "外滩"),
                    "tips": "建议早点到达，避开人流高峰，可以拍到更美的照片"
                },
                {
                    "time": "09:30-11:00",
                    "activity": "外滩漫步 + 南京路步行街",
                    "location": "外滩 → 南京路步行街",
                    "description": "沿着外滩漫步，欣赏黄浦江两岸风光，然后前往南京路步行街购物",
                    "attraction": self._find_attraction(attractions, "南京路"),
                    "tips": "南京路步行街是上海最著名的商业街，可以购买一些上海特产"
                },
                {
                    "time": "11:00-12:30",
                    "activity": "豫园 + 城隍庙",
                    "location": "豫园及城隍庙商圈",
                    "description": "游览古典园林豫园，体验传统建筑艺术，在城隍庙品尝上海小吃",
                    "attraction": self._find_attraction(attractions, "豫园"),
                    "tips": "豫园需要门票，建议提前购买。城隍庙小吃街有很多上海特色美食"
                },
                {
                    "time": "12:30-13:30",
                    "activity": "前往陆家嘴",
                    "location": "陆家嘴金融区",
                    "description": "乘坐地铁或轮渡前往浦东陆家嘴，沿途可以休息",
                    "attraction": self._find_attraction(attractions, "陆家嘴"),
                    "tips": "可以乘坐2号线地铁，或者体验黄浦江轮渡（推荐，风景好）"
                },
                {
                    "time": "13:30-15:30",
                    "activity": "东方明珠 / 上海中心大厦",
                    "location": "陆家嘴",
                    "description": "登高俯瞰上海全景，感受现代化都市的魅力",
                    "attraction": self._find_attraction(attractions, "东方明珠"),
                    "tips": "建议提前网上购票，避免排队。上海中心大厦是上海第一高楼"
                },
                {
                    "time": "15:30-17:00",
                    "activity": "世纪公园（可选）",
                    "location": "世纪公园",
                    "description": "如果天气好，可以在世纪公园放松，体验自然与城市的融合",
                    "attraction": self._find_attraction(attractions, "世纪公园"),
                    "tips": "如果时间紧张或天气不好，可以跳过此景点，直接前往晚餐地点"
                },
                {
                    "time": "17:00-18:30",
                    "activity": "晚餐",
                    "location": "陆家嘴或外滩",
                    "description": "在黄浦江畔的景观餐厅享用晚餐，品尝上海本帮菜或国际美食",
                    "attraction": None,
                    "tips": "推荐外滩18号、外滩3号等景观餐厅，需要提前预订"
                },
                {
                    "time": "18:30-20:00",
                    "activity": "黄浦江夜游 / 外滩夜景",
                    "location": "外滩",
                    "description": "欣赏黄浦江两岸的璀璨夜景，外滩建筑群在灯光下格外迷人",
                    "attraction": self._find_attraction(attractions, "外滩"),
                    "tips": "夜晚的外滩是上海最美的风景，建议多拍照片留念"
                },
                {
                    "time": "20:00-21:00",
                    "activity": "新天地夜生活",
                    "location": "新天地",
                    "description": "在新天地感受上海的夜生活，可以选择酒吧或咖啡厅放松",
                    "attraction": self._find_attraction(attractions, "新天地"),
                    "tips": "新天地是上海时尚地标，有很多特色酒吧和餐厅"
                }
            ],
            "transportation": {
                "地铁": "建议购买地铁一日票，方便快捷",
                "轮渡": "外滩到陆家嘴可以乘坐轮渡，体验黄浦江风光",
                "步行": "外滩、南京路、豫园等景点之间可以步行"
            },
            "food_recommendations": {
                "早餐": ["生煎包", "小笼包", "灌汤包", "豆浆油条"],
                "午餐": ["南翔小笼包", "本帮菜", "上海小馄饨", "生煎馒头"],
                "晚餐": ["上海本帮菜", "黄浦江景观餐厅", "国际美食"]
            },
            "tips": [
                "带好身份证，部分景点需要实名制",
                "建议使用微信/支付宝扫码乘地铁",
                "避开12:00-14:00和17:00-19:00的交通高峰",
                "提前预订热门景点门票（如东方明珠、上海中心）",
                "注意天气变化，带好雨具",
                "外滩和陆家嘴是拍照的最佳地点"
            ]
        }
        
        return itinerary
    
    def _find_attraction(self, attractions: List[Dict], keyword: str) -> Optional[Dict]:
        """在景点列表中查找包含关键词的景点"""
        for attr in attractions:
            if keyword in attr.get("name", ""):
                return attr
        return None
    
    def print_itinerary(self, itinerary: Dict):
        """打印旅游攻略"""
        print("\n" + "="*60)
        print(f"📅 上海一天旅游攻略 - {itinerary['date']}")
        print("="*60 + "\n")
        
        print("🗓️ 行程安排：\n")
        for i, item in enumerate(itinerary['schedule'], 1):
            print(f"{i}. 【{item['time']}】{item['activity']}")
            print(f"   地点：{item['location']}")
            print(f"   说明：{item['description']}")
            if item.get('attraction'):
                attr = item['attraction']
                print(f"   地址：{attr.get('address', '未知')}")
                if attr.get('rating'):
                    print(f"   评分：{attr.get('rating')}")
            if item.get('tips'):
                print(f"   💡 提示：{item['tips']}")
            print()
        
        print("\n" + "="*60)
        print("🚇 交通建议：")
        print("="*60)
        for key, value in itinerary['transportation'].items():
            print(f"   {key}：{value}")
        
        print("\n" + "="*60)
        print("🍜 美食推荐：")
        print("="*60)
        for meal, foods in itinerary['food_recommendations'].items():
            print(f"   {meal}：{', '.join(foods)}")
        
        print("\n" + "="*60)
        print("💡 实用提示：")
        print("="*60)
        for tip in itinerary['tips']:
            print(f"   • {tip}")
        
        print("\n" + "="*60)
        print("祝您旅途愉快！🎉")
        print("="*60 + "\n")
    
    def save_itinerary_json(self, itinerary: Dict, filename: str = "shanghai_itinerary.json"):
        """保存攻略为JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(itinerary, f, ensure_ascii=False, indent=2)
        print(f"✓ 攻略已保存到 {filename}")


def main():
    """主函数"""
    # 注意：需要替换为你的高德地图API Key
    # 申请地址：https://lbs.amap.com/api/webservice/summary
    API_KEY = "YOUR_AMAP_API_KEY"  # 请替换为你的API Key
    
    if API_KEY == "YOUR_AMAP_API_KEY":
        print("⚠️  请先设置高德地图API Key！")
        print("   1. 访问 https://lbs.amap.com/api/webservice/summary")
        print("   2. 注册并申请API Key")
        print("   3. 在代码中替换 API_KEY 变量")
        print("\n   现在将使用模拟数据生成攻略...\n")
        
        # 使用模拟数据
        guide = AmapTravelGuide("demo_key")
        itinerary = guide.generate_one_day_itinerary()
        guide.print_itinerary(itinerary)
        guide.save_itinerary_json(itinerary)
    else:
        guide = AmapTravelGuide(API_KEY)
        itinerary = guide.generate_one_day_itinerary()
        guide.print_itinerary(itinerary)
        guide.save_itinerary_json(itinerary)


if __name__ == "__main__":
    main()
