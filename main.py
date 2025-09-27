import asyncio
from pyrogram import Client
from app.utils.detector import cleaner
from app.utils.logger import logger
from data.config import config


class Application:
    @staticmethod
    async def run() -> None:
        async with Client(
                name=config.SESSION,
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                phone_number=config.PHONE_NUMBER
        ) as client:
            await cleaner(client)

    @staticmethod
    def main() -> None:
        try:
            asyncio.run(Application.run())
        except Exception as ex:
            logger.error(f'Произошла ошибка: {ex}')


Application.main() if __name__ == "__main__" else None
