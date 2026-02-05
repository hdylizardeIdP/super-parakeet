FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Wait for postgres, run migrations/seed, then start server
CMD ["sh", "-c", "sleep 3 && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
