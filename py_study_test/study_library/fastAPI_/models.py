from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# 用户角色枚举
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# 请求模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: str = Field(..., min_length=8, description="密码")
    role: UserRole = UserRole.USER
    age: Optional[int] = Field(None, ge=0, le=150)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "secure_password123",
                "role": "user",
                "age": 25
            }
        }

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    role: Optional[UserRole] = None
    age: Optional[int] = Field(None, ge=0, le=150)

# 响应模型
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    age: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # 允许从 ORM 模型转换

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int

# 错误响应模型
class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
    detail: Optional[str] = None

# 分页查询参数
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=100, description="每页大小")
    
    class Config:
        extra = "forbid"  # 禁止额外字段