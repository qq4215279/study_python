from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from datetime import datetime

# 简化版本 - 避免复杂的中间件问题
app = FastAPI(
    title="FastAPI 简化学习示例",
    description="FastAPI 核心功能演示",
    version="1.0.0"
)

# 数据模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: Optional[int]
    created_at: str

# 模拟数据库
fake_users_db = {}
user_counter = 1

# 基础路由
@app.get("/")
async def root():
    return {
        "message": "欢迎使用 FastAPI!",
        "features": [
            "自动 API 文档",
            "数据验证",
            "依赖注入",
            "异步支持"
        ],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# 用户管理 API
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    global user_counter
    
    # 检查用户名是否存在
    for existing_user in fake_users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(status_code=409, detail="用户名已存在")
    
    # 创建用户
    user_data = {
        "id": user_counter,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "created_at": str(datetime.now())
    }
    
    fake_users_db[user_counter] = user_data
    user_counter += 1
    
    return UserResponse(**user_data)

@app.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 10):
    users = list(fake_users_db.values())[skip: skip + limit]
    return [UserResponse(**user) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    return UserResponse(**fake_users_db[user_id])

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户信息
    fake_users_db[user_id].update({
        "username": user_update.username,
        "email": user_update.email,
        "age": user_update.age
    })
    
    return UserResponse(**fake_users_db[user_id])

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    del fake_users_db[user_id]
    return

# 依赖注入示例
async def get_user_by_id(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    return fake_users_db[user_id]

@app.get("/users/{user_id}/info")
async def get_user_info(user_data: dict = Depends(get_user_by_id)):
    return {
        "user_info": user_data,
        "request_time": str(datetime.now())
    }

# 查询参数示例
@app.get("/search")
async def search_users(q: Optional[str] = None, age_min: Optional[int] = None):
    results = []
    for user in fake_users_db.values():
        if q and q.lower() not in user["username"].lower():
            continue
        if age_min and (user["age"] is None or user["age"] < age_min):
            continue
        results.append(user)
    return {"results": results, "count": len(results)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")