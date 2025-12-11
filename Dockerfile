FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && gunicorn -w 2 -b 0.0.0.0:5000 run:app"]
