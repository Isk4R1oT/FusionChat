from backend.api.endpoints import router
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

app.include_router(router, prefix='/api')

# Монтируем папку static для раздачи всех статических файлов
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

# Определяем маршрут для отображения главной страницы (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = Path("frontend/static/index.html")
    if not index_path.exists():
        return HTMLResponse(content="<h1>index.html не найден</h1>", status_code=404)
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))