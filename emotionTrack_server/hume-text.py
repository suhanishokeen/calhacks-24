import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamLanguage
import json

samples = [
    "Mary had a little lamb,",
    "Its fleece was white as snow."
    "Everywhere the child went,"
    "The little lamb was sure to go."
]

async def main():
    client = AsyncHumeClient(api_key="cA4UwmmxaQ0GzIwfriZontAeewATKGIX4z5xHDy5mKRq9WRJ")

    model_config = Config(language=StreamLanguage())

    stream_options = StreamConnectOptions(config=model_config)

    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        for sample in samples:
            result = await socket.send_text(sample)
            for prediction in result.language.predictions:
                print(f"Text: {prediction.text}")
                print("Emotions:")
                for emotion in prediction.emotions:
                    print(f"  {emotion.name}: {emotion.score}")
                print("---")

if __name__ == "__main__":
    asyncio.run(main())
