import itertools

import grpc

import weather_pb2
import weather_pb2_grpc

servers = itertools.cycle(["server1:50051", "server2:50052"])


def get_temperature_for_city(client, city):
    server_address = next(servers)
    print(f"Requesting {city} temperature from {server_address}")

    channel = grpc.insecure_channel(server_address)
    stub = weather_pb2_grpc.WeatherServiceStub(channel)

    response = stub.GetTemperature(weather_pb2.CityRequest(city=city))

    print(f"Received temperature for {response.city}: {response.temperature}°C")

    channel.close()


if __name__ == "__main__":
    city = "Tunis"

    for i in range(4):
        get_temperature_for_city(i, city)
