FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .

ENV HOST=0.0.0.0
EXPOSE 8060

CMD ["python", "server.py"]
