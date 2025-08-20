FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 7101

CMD ["python", "-m", "uvicorn", "app:APP", "--host", "0.0.0.0", "--port", "7101"]