from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import logging
import time
from typing import Callable
import uuid

# 高级日志配置
class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: logging.Logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable):
        # 生成请求 ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # 记录请求开始
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        
        self.logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"from {client_ip}"
        )
        
        # 处理请求
        response = await call_next(request)
        
        # 记录响应信息
        process_time = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        self.logger.info(
            f"[{request_id}] Response: {response.status_code} "
            f"in {process_time:.4f}s"
        )
        
        return response

# 请求验证中间件
class RequestValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # 验证请求头
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if "application/json" not in content_type:
                return Response(
                    content='{"error": "Content-Type must be application/json"}',
                    status_code=400,
                    media_type="application/json"
                )
        
        # 继续处理请求
        response = await call_next(request)
        return response

# 安全头中间件
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # 添加安全相关的响应头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

# 速率限制中间件（简化版）
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # 简化的内存存储
    
    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # 清理过期记录
        expired_keys = []
        for ip, timestamps in self.requests.items():
            self.requests[ip] = [ts for ts in timestamps if current_time - ts < self.window_seconds]
            if not self.requests[ip]:
                expired_keys.append(ip)
        
        for key in expired_keys:
            del self.requests[key]
        
        # 检查速率限制
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        self.requests[client_ip].append(current_time)
        
        if len(self.requests[client_ip]) > self.max_requests:
            return Response(
                content='{"error": "Rate limit exceeded"}',
                status_code=429,
                media_type="application/json"
            )
        
        return await call_next(request)

# 配置日志格式化器
def setup_logging():
    """配置详细的日志系统"""
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)

# 使用示例函数
def add_middlewares_to_app(app: FastAPI):
    """将所有中间件添加到 FastAPI 应用"""
    logger = setup_logging()
    
    # 按顺序添加中间件（注意顺序很重要）
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests=50, window_seconds=60)
    app.add_middleware(RequestValidationMiddleware)
    app.add_middleware(LoggingMiddleware, logger=logger)
    
    return app