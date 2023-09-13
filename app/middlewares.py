import time
from logging import Logger

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send, Message


# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logger.info("Request process time", extra={
#         "process_time": round(process_time, 4),
#         "path": request.url
#     })
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """
    Добавляет в HTTP-ответ заголовок X-Process-Time с временем обработки
    запроса в секундах и добавляет его в лог, если задан параметр **app_logger**
    """
    def __init__(self, app: ASGIApp, app_logger: Logger = None):
        super().__init__(app)
        self.logger = app_logger
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = round(time.time() - start_time, 4)
        if self.logger:
            self.logger.info("Request process time", extra={
                "process_time": process_time,
                "path": request.url
            })
        response.headers["X-Process-Time"] = str(process_time)
        return response


# class ProcessTimeMiddleware2:
#     def __init__(self, app: ASGIApp) -> None:
#         self.app = app
#
#     async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
#         if scope["type"] != "http":
#             return await self.app(scope, receive, send)
#
#         start_time = time.time()
#         await self.app(scope, receive, send)
#         process_time = time.time() - start_time
#         logger.info("Request process time", extra={
#             "process_time": round(process_time, 4),
#             "path": scope["path"],
#             "query": scope["query_string"].decode()
#         })
#