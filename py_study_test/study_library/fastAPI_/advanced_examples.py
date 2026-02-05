"""
FastAPI 核心特性演示文件
包含各种高级特性和最佳实践示例
"""

from fastapi import FastAPI, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import asyncio
import os
from datetime import datetime, timedelta
from enum import Enum

app = FastAPI(title="FastAPI 高级特性演示")

# ==================== 1. 安全认证示例 ====================
security = HTTPBearer()

class TokenData(BaseModel):
    username: str
    scopes: List[str] = []

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT token 验证示例"""
    # 实际项目中这里会解析和验证 JWT token
    if credentials.credentials != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "authenticated_user", "scopes": ["read", "write"]}

# ==================== 2. 表单数据处理 ====================
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """表单登录示例"""
    return {"username": username, "message": "登录成功"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Form(None)
):
    """文件上传示例"""
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "description": description,
        "size": file.size
    }

# ==================== 3. WebSocket 支持 ====================
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 连接示例"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"收到消息: {data}")
    except Exception as e:
        print(f"WebSocket 错误: {e}")

# ==================== 4. 后台任务 ====================
from fastapi.concurrency import run_in_threadpool

def write_log(message: str):
    """后台写入日志"""
    with open("background_tasks.log", "a") as f:
        f.write(f"{datetime.now()}: {message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """发送通知（后台任务示例）"""
    background_tasks.add_task(write_log, f"发送邮件给 {email}")
    return {"message": f"通知已加入队列，将发送给 {email}"}

# ==================== 5. 缓存装饰器 ====================
from functools import lru_cache

@lru_cache(maxsize=128)
def get_expensive_data(item_id: int) -> Dict[str, Any]:
    """模拟耗时的数据获取操作"""
    # 模拟耗时操作
    import time
    time.sleep(1)
    return {"item_id": item_id, "data": f"昂贵的数据_{item_id}", "cached": True}

@app.get("/expensive-data/{item_id}")
async def get_cached_data(item_id: int):
    """获取缓存数据"""
    return get_expensive_data(item_id)

# ==================== 6. 条件依赖 ====================
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

async def require_role(required_role: UserRole):
    """角色权限检查依赖工厂"""
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if required_role == UserRole.ADMIN and "admin" not in current_user.get("scopes", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        return current_user
    return role_checker

@app.get("/admin/data")
async def admin_only_data(
    current_user: dict = Depends(require_role(UserRole.ADMIN))
):
    """仅管理员可访问的端点"""
    return {"message": "管理员数据", "user": current_user}

# ==================== 7. 响应模型继承 ====================
class BaseEntity(BaseModel):
    id: int
    created_at: datetime

class UserEntity(BaseEntity):
    username: str
    email: str

class ProductEntity(BaseEntity):
    name: str
    price: float

@app.get("/entities/users", response_model=List[UserEntity])
async def get_users_entities():
    """返回用户实体列表"""
    return [
        UserEntity(
            id=1,
            username="user1",
            email="user1@example.com",
            created_at=datetime.now()
        )
    ]

# ==================== 8. 自定义响应类型 ====================
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    """返回 HTML 响应"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI HTML 示例</title>
    </head>
    <body>
        <h1>欢迎使用 FastAPI!</h1>
        <p>这是 HTML 响应示例</p>
    </body>
    </html>
    """
    return html_content

# ==================== 9. 请求体多个模型 ====================
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

@app.post("/items-and-user/")
async def create_item_and_user(item: Item, user: User):
    """同时接收多个请求体模型"""
    return {"item": item, "user": user}

# ==================== 10. 嵌套模型 ====================
class Image(BaseModel):
    url: str
    name: str

class ItemWithImages(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    images: List[Image] = []

@app.post("/items-with-images/", response_model=ItemWithImages)
async def create_item_with_images(item: ItemWithImages):
    """带嵌套模型的请求处理"""
    return item

# ==================== 11. 路径操作配置 ====================
@app.get(
    "/configured-endpoint",
    summary="配置化的端点",
    description="这是一个展示了多种配置选项的端点",
    response_description="返回配置信息",
    status_code=status.HTTP_200_OK,
    tags=["配置示例"],
    deprecated=False
)
async def configured_endpoint():
    """带有详细配置的端点示例"""
    return {
        "message": "这是一个配置化的端点",
        "configurations": [
            "summary", "description", "response_description",
            "status_code", "tags", "deprecated"
        ]
    }

# ==================== 12. API 版本控制 ====================
@app.get("/api/v1/users")
async def get_users_v1():
    """API v1 版本"""
    return {"version": "v1", "users": ["user1", "user2"]}

@app.get("/api/v2/users")
async def get_users_v2():
    """API v2 版本"""
    return {"version": "v2", "users": [{"id": 1, "name": "user1"}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)