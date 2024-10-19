import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions

async def main():
    client = AsyncHumeClient(api_key="cA4UwmmxaQ0GzIwfriZontAeewATKGIX4z5xHDy5mKRq9WRJ")

    model_config = Config(prosody={})

    stream_options = StreamConnectOptions(config=model_config)

    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file("The Moscone Center.m4a")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
