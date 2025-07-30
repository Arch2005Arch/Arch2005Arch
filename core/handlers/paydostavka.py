from aiogram import Bot
from aiogram.types import (
    Message, PreCheckoutQuery, ShippingQuery,
    LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton,
    ShippingOption
)


# Клавиатура с кнопкой оплаты и ссылкой
payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить заказ', pay=True)],
    [InlineKeyboardButton(text='Контакты', url='https://t.me/Arc_2010')]
])

# Опции доставки
RU_SHIPPING = ShippingOption(
    id='ru',
    title='Доставка по России',
    prices=[LabeledPrice(label='Доставка Почтой России', amount=500)]
)

BY_SHIPPING = ShippingOption(
    id='by',
    title='Доставка по Беларуси',
    prices=[LabeledPrice(label='Доставка Белпочтой', amount=500)]
)

UA_SHIPPING = ShippingOption(
    id='ua',
    title='Доставка по Украине',
    prices=[LabeledPrice(label='Доставка Укрпочтой', amount=500)]
)

CITY_SHIPPING = ShippingOption(
    id='capitals',
    title='Экспресс-доставка по городу',
    prices=[LabeledPrice(label='Курьерская доставка', amount=2000)]
)

# Проверка и выбор доступных методов доставки
async def shipping_check(shipping_query: ShippingQuery, bot: Bot):
    allowed_countries = ['BY', 'RU', 'UA']
    shipping_options = []

    country = shipping_query.shipping_address.country_code
    city = shipping_query.shipping_address.city

    if country not in allowed_countries:
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message='Мы не доставляем в вашу страну.'
        )

    if country == 'BY':
        shipping_options.append(BY_SHIPPING)
    elif country == 'RU':
        shipping_options.append(RU_SHIPPING)
    elif country == 'UA':
        shipping_options.append(UA_SHIPPING)

    express_cities = ['Минск', 'Москва', 'Киев']
    if city in express_cities:
        shipping_options.append(CITY_SHIPPING)

    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )

# Отправка счета пользователю
async def create_orders(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка цифрового продукта',
        description='Получите доступ к эксклюзивному контенту через Telegram-бота.',
        payload='internal_payment_payload',
        provider_token='2051251535:TEST:OTk5MDA4ODgxLTAwNQ',  # замените на рабочий токен
        currency='UAH',
        prices=[
            LabeledPrice(label='Доступ к материалам', amount=99000),
            LabeledPrice(label='НДС', amount=20000),
            LabeledPrice(label='Скидка', amount=-20000),
            LabeledPrice(label='Бонус', amount=-40000)
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter='unique_start_param',
        provider_data=None,
        photo_url=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=True,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=payment_keyboard,
        request_timeout=15
    )

# Подтверждение готовности к оплате (обязательный хендлер)
async def handle_pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Уведомление пользователя об успешной оплате
async def handle_successful_payment(message: Message):
    total = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    await message.answer(
        f'Спасибо за оплату! Вы оплатили {total} {currency}.\n'
        f'Ссылка на ваш продукт или инструкция будет выслана в ближайшее время.'
    )
