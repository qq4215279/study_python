from fastapi import FastAPI, HTTPException, Depends, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
import uvicorn
import logging
from datetime import datetime
import time

from models import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
    ErrorResponse, PaginationParams, UserRole
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="FastAPI 学习示例",
    description="这是一个展示 FastAPI 核心特性的学习项目",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI 文档路径
    redoc_url="/redoc",      # ReDoc 文档路径
    openapi_url="/openapi.json"  # OpenAPI schema 路径
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据库存储
fake_users_db = {}
user_id_counter = 1

# ==================== 中间件示例 ====================
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """记录请求处理时间的中间件"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request: {request.method} {request.url} - Process Time: {process_time:.4f}s")
    return response

# ==================== 依赖注入示例 ====================
async def get_current_user(token: str = None):
    """模拟获取当前用户"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证令牌"
        )
    # 这里可以实现真实的 JWT 解析逻辑
    return {"user_id": 1, "username": "test_user"}

async def get_pagination_params(page: int = 1, size: int = 10) -> PaginationParams:
    """分页参数依赖"""
    return PaginationParams(page=page, size=size)

def require_admin(current_user: dict = Depends(get_current_user)):
    """管理员权限检查依赖"""
    # 这里可以检查用户角色
    return current_user

# ==================== 基础路由示例 ====================
@app.get("/")
async def root():
    """根路径 - 返回欢迎信息"""
    return {
        "message": "欢迎使用 FastAPI 学习示例！",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ==================== 用户管理 API ====================
@app.post("/users", 
          response_model=UserResponse,
          status_code=status.HTTP_201_CREATED,
          summary="创建新用户",
          description="创建一个新的用户账户")
async def create_user(user: UserCreate):
    """创建用户"""
    global user_id_counter
    
    # 检查用户名是否已存在
    for existing_user in fake_users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"用户名 '{user.username}' 已存在"
            )
    
    # 创建新用户
    user_data = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
        "age": user.age,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "password": user.password  # 实际项目中应该加密存储
    }
    
    fake_users_db[user_id_counter] = user_data
    user_id_counter += 1
    
    logger.info(f"Created user: {user.username}")
    return UserResponse(**user_data)

@app.get("/users", response_model=UserListResponse)
async def get_users(
    pagination: PaginationParams = Depends(get_pagination_params),
    role: Optional[UserRole] = None
):
    """获取用户列表（支持分页和角色筛选）"""
    # 筛选用户
    filtered_users = list(fake_users_db.values())
    if role:
        filtered_users = [u for u in filtered_users if u["role"] == role.value]
    
    # 分页处理
    total = len(filtered_users)
    start_idx = (pagination.page - 1) * pagination.size
    end_idx = start_idx + pagination.size
    paginated_users = filtered_users[start_idx:end_idx]
    
    # 转换为响应模型（移除密码字段）
    users_response = []
    for user_data in paginated_users:
        user_copy = user_data.copy()
        user_copy.pop("password", None)  # 移除密码字段
        users_response.append(UserResponse(**user_copy))
    
    return UserListResponse(
        users=users_response,
        total=total,
        page=pagination.page,
        size=pagination.size
    )

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """根据 ID 获取单个用户"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 ID {user_id} 不存在"
        )
    
    user_data = fake_users_db[user_id].copy()
    user_data.pop("password", None)  # 移除密码字段
    return UserResponse(**user_data)

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """更新用户信息"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 ID {user_id} 不存在"
        )
    
    # 更新用户数据
    user_data = fake_users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            user_data[field] = value
    
    user_data["updated_at"] = datetime.now()
    
    # 如果更新了用户名，检查是否重复
    if user_update.username and user_update.username != user_data["username"]:
        for uid, existing_user in fake_users_db.items():
            if uid != user_id and existing_user["username"] == user_update.username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"用户名 '{user_update.username}' 已存在"
                )
    
    logger.info(f"Updated user {user_id}: {user_data['username']}")
    user_response = user_data.copy()
    user_response.pop("password", None)
    return UserResponse(**user_response)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: dict = Depends(require_admin)  # 需要管理员权限
):
    """删除用户（需要管理员权限）"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 ID {user_id} 不存在"
        )
    
    deleted_user = fake_users_db.pop(user_id)
    logger.info(f"Deleted user {user_id}: {deleted_user['username']}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ==================== 自定义异常处理器 ====================
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """自定义 HTTP 异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ErrorResponse(
            error_code=exc.status_code,
            error_message=exc.detail
        ))
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(ErrorResponse(
            error_code=500,
            error_message="服务器内部错误",
            detail=str(exc) if app.debug else None
        ))
    )

# ==================== 启动配置 ====================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式下自动重载
        log_level="info"
    )