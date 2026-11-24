# app/main.py
import time

from fastapi import FastAPI, Request

from app.config import API_PREFIX, APP_TITLE, APP_VERSION
from app.routers import authors, books

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Middleware логирования
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    return response

# Healthcheck
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# Подключение роутеров
app.include_router(books.router, prefix=API_PREFIX)
app.include_router(authors.router, prefix=API_PREFIX)