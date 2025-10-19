FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install grpcio grpcio-tools

EXPOSE 50051
EXPOSE 50052

CMD ["python", "weather_server_1.py"]
