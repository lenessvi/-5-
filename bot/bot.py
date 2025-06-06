import logging
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, API_URL

from aiogram import Router, Dispatcher
from aiogram.utils.markdown import hbold
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import types
from aiogram import Bot
import asyncio
from io import BytesIO

router = Router()
bot = Bot(token=BOT_TOKEN, session=AiohttpSession())
dp = Dispatcher()
dp.include_router(router)

@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("Фото получено, определяю эмоцию...")

    photo = message.photo[-1]
    photo_bytes = await bot.download(photo.file_id)

    form = aiohttp.FormData()
    form.add_field("image", photo_bytes, filename="photo.jpg", content_type="image/jpeg")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, data=form) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    emotion = result.get("emotion", "неизвестно")
                    await message.answer(f"Эмоция животного: {emotion}")
                else:
                    await message.answer("Ошибка при обработке изображения.")
        except Exception as e:
            await message.answer(f"Ошибка соединения с API: {e}")

@router.message(F.text)
async def fallback(message: Message):
    await message.answer("Отправь, пожалуйста, фото животного 🐶")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
