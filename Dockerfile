FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY app ./app
COPY data/sample_code ./data/sample_code
COPY data/evaluation ./data/evaluation
COPY scripts ./scripts
COPY static ./static
COPY run.py README.md ./

RUN mkdir -p data/index
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
