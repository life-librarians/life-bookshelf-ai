FROM python:3.9

RUN mkdir -p /app/serve/

WORKDIR /app/serve/

COPY serve/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt keyrings.alt

COPY ./serve/ /app/serve/
COPY ./flows/ /app/flows/

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
