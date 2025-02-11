import subprocess
import os

# Путь к основному файлу FastAPI
FASTAPI_MODULE = "backend.main:app"  # Укажите правильный путь к вашему приложению

# Настройки сервера
FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = 8000
FASTAPI_WORKERS = 4  # Количество воркеров

def main():
    try:
        print(f"Запуск FastAPI на http://localhost:{FASTAPI_PORT} с {FASTAPI_WORKERS} воркерами...")
        fastapi_process = subprocess.Popen(
            [
                "uvicorn",
                FASTAPI_MODULE,
                "--host", FASTAPI_HOST,
                "--port", str(FASTAPI_PORT),
                "--workers", str(FASTAPI_WORKERS)
            ],
            env=os.environ
        )

        fastapi_process.wait()  # Ожидаем завершения процесса

    except KeyboardInterrupt:
        print("Остановка FastAPI сервера...")
        fastapi_process.terminate()

if __name__ == "__main__":
    main()