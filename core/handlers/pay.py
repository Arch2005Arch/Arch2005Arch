from aiogram import Bot
from aiogram.types import (
    Message, PreCheckoutQuery, LabeledPrice,
    ShippingQuery, ShippingOption,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# Хендлер для отправки инвойса (счёта на оплату)
async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка через Telegram-бота',
        description='Платеж через телеграм бот',
        payload='payment_through_bot',
        provider_token='2051251535:TEST:OTk5MDA4ODgxLTAwNQ',  # тестовый токен от BotFather
        currency='UAH',
        prices=[
            LabeledPrice(label='Доступ к секретной информации', amount=99000),
            LabeledPrice(label='НДС', amount=20000),
            LabeledPrice(label='Скидка', amount=-20000),
            LabeledPrice(label='Бонус', amount=-40000),
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter='carro_pogoda_bot',
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )

# Хендлер для обработки запроса перед оплатой
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Хендлер для подтверждения успешной оплаты
async def successful_payment(message: Message):
    total = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    await message.answer(
        f'✅ Спасибо за оплату {total} {currency}!\n'
        f'📞 Наш менеджер получил заявку и уже набирает ваш номер телефона.'
    )
