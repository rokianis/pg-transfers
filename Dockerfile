FROM python:3.9-slim

WORKDIR /app
COPY app/ .

RUN pip install fastapi uvicorn python-multipart aiofiles

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]