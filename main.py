"""Entry point for running the Telegram bot."""
from aiogram import executor

from handlers import dp
from loader import bot


async def on_shutdown(dispatcher):
    await bot.close()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)
