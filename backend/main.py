from backend.api.endpoints import router
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

app.include_router(router, prefix='/api')


app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Обслуживаем index.html из корневой директории
@app.get("/", response_class=FileResponse)
async def read_index():
    index_path = Path("index.html")
    return FileResponse(index_path)