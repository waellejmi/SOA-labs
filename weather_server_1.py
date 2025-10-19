import time
from concurrent import futures

import grpc

import weather_pb2
import weather_pb2_grpc


class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(self, temperature):
        self.temperature = temperature

    def GetTemperature(self, request, context):
        print(f"Received request for city: {request.city}")
        return weather_pb2.TemperatureResponse(
            city=request.city, temperature=self.temperature
        )


def serve(port, temperature):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(
        WeatherService(temperature), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started on port {port} with temperature {temperature}°C")
    return server


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50051
    temperature = float(sys.argv[2]) if len(sys.argv) > 2 else 26.0
    server = serve(port, temperature)
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
