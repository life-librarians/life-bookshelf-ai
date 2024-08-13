FROM python:3.9

WORKDIR /app

COPY serve/requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./serve/ /app
COPY ./flows/ /app

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--env-file", ".env.production"]
