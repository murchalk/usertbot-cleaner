import asyncio
from pyrogram import Client
from data.config import config
from app.utils.logger import logger
from datetime import datetime, timedelta


class Cleaner:
    @staticmethod
    async def run_clean(app: Client) -> None:
        logger.info('Запуск цикла.')

        try:
            await app.get_users(config.CHATS_ID)
        except:
            logger.warn(f'Не найдены все чаты (или один из них) в конфиге. Идет загрузка диалогов в сессию.')
            async for _ in app.get_dialogs():
                continue

        for chat_id in config.CHATS_ID:
            logger.info(f'Началась обработка чата {chat_id}')
            try:
                await app.get_chat(chat_id)
            except:
                logger.error(f'Не удалось найти чат {chat_id} после загрузки диалогов в сессию. Проверьте корректность идентификатора.')
                continue

            async for msg in app.get_chat_history(chat_id, limit=config.COUNT_MESSAGES):
                if config.LIMIT_HOURS and config.LIMIT_HOURS > 0:
                    msg_age = datetime.utcnow() - msg.date
                    if msg_age > timedelta(hours=config.LIMIT_HOURS):
                        break

                if msg.from_user and msg.from_user.is_self:
                    logger.info(f'Зачищаю сообщение: {msg.id}')
                    try:
                        await msg.edit_text(config.TEXT_REPLACE)
                    except:
                        logger.warn('Ошибка редактирования.')

                    try:
                        await app.delete_messages(chat_id, msg.id)
                    except:
                        logger.warn('Ошибка удаления.')

                    await asyncio.sleep(config.INTERVAL_MESSAGE)
            await asyncio.sleep(config.INTERVAL_CHAT)
        logger.info('Цикл работы завершен.')

cleaner = Cleaner.run_clean
