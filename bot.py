import asyncio

from aiogram import Bot, Dispatcher,Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from cryptomus import create_invoice,get_invoice

router = Router()

@router.message(CommandStart())
async def start(message: Message)->None:
    invoice = await create_invoice(message.from_user.id,currency=10)
    markup = InlineKeyboardBuilder().button(text = 'Check',callback_data=f"o_{invoice['result']['uuid']}")

    await message.answer(
        f'{invoice['result']['url']}',
        reply_markup=markup.as_markup()
                         )


@router.callback_query(F.data.startswith('o_'))
async def check_order(query: CallbackQuery)->None:
    invoice  = await get_invoice(query.data.split('_')[1])

    if invoice['result']['status'] == 'paid':
        await query.message.answer('Paid')
        await query.answer()
    else:
        await query.answer('Not paid')

async def main()->None:
    bot = Bot(token="TOKEN")

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot,skip_updates = True)
    await bot.delete_webhook(True)


if __name__ == "__main__":
    asyncio.run(main())