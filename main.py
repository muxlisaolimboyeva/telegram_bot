import asyncio
import time

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
import os
from aiogram.filters import Command

from configs import get_value
from keyboards import buttons_category
from open_pars import pars_texno

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(
    TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start(message: Message):
    full_name = message.from_user.full_name
    await message.answer(
        f"Salom <b>{full_name}</b>!\n"
        f"Openshop ga xush kelibsiz 🚀"
    )
    await show_category_menu(message)


async def show_category_menu(message: Message):
    await message.answer("Kategoriya tanlang 👇", reply_markup=buttons_category())


@dp.message()
async def get_product_by_open_shop(message: Message):
    category_text = message.text

    category_key = get_value(category_text)
    if category_key is None:
        return await message.answer(
            "Kechirasiz, bunday kategoriya mavjud emas!\n"
            "Iltimos tugmalardan birini tanlang 👇"
        )

    get_product = pars_texno(category_key)
    if not get_product:
        return await message.answer("⚠ Ushbu kategoriyada mahsulot topilmadi!")

    for product in get_product:
        image = product.get('images')
        title = product.get('title')
        credit_price = product.get('credit_price')
        price = product.get('price')

        time.sleep(0.5)

        await message.answer_photo(
            photo=image,
            caption=f"{title}\n\n{credit_price}\n\n{price}",
        )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
