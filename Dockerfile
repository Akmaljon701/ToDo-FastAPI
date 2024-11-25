FROM python:3.10

WORKDIR /app

COPY . /app/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.app.main:app --host 0.0.0.0 --port 8000"]
