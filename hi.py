# from ast import pattern
import os
from xml.sax.handler import EntityResolver
# from telegram.constants import ParseMode

from dotenv import load_dotenv
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                      InlineQueryResult, InlineQueryResultArticle, InlineQueryResultVoice, InputMediaPhoto,
                      InputTextMessageContent, Invoice, MenuButton,
                      ReplyKeyboardRemove, ReplyMarkup, SuccessfulPayment, Update, LabeledPrice, InputInvoiceMessageContent, ShippingOption)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, InlineQueryHandler, Updater,
                          ShippingQueryHandler, PreCheckoutQueryHandler, MessageHandler, Filters)

load_dotenv()
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')
bot = Bot(token=os.getenv('TOKEN'))
keyboard = [[
    InlineKeyboardButton('Продолжить', callback_data='1'),
]]
bot = Bot(token=os.getenv('TOKEN'))
updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Собаки", callback_data="Собаки"),
            InlineKeyboardButton("Наруто Узумаки", callback_data="Наруто Узумаки"),
        ],
        [InlineKeyboardButton("Не собаки", callback_data="Не собаки")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def send_message(user_id, message, **kwargs):
    return bot.send_message(chat_id=user_id, text=message, **kwargs)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    bot.send_invoice(
        update.message.chat_id,
        'title',
        'description',
        'payload',
        PAYMENT_PROVIDER_TOKEN,
        currency='RUB',
        prices = [LabeledPrice('price', 32200)],
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )
    # query = update.callback_query
    # user = update.effective_user.id
    # send_message(user, f'йоу {query.data}')
    # print(f'юзерайди = {user}')
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # query.answer()

    # query.delete_message()


def inline_query(update: Update, context: CallbackContext) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    # First option has a single LabeledPrice
    # options = [ShippingOption('1', 'Голубиная почта', [LabeledPrice('2 жирных голубя', 1000000)]),
    #            ShippingOption('2', 'Почта России', [LabeledPrice('Почта России', 9000)]),
    #            ShippingOption('3', 'Почта России (экспресс)', [LabeledPrice('Почта России (экспресс)', 148800)])]
    results = [
        # InlineQueryResultArticle(
        #     id='1',
        #     title="большой текст",
        #     input_message_content = InputTextMessageContent('оно работает боже как же заебись'),
        #     thumb_url = 'https://2ch.hk/b/src/266160769/16492546145510.png',
        # ),
        InlineQueryResultArticle(
            id = '1',
            title = 'Модная кепка',
            thumb_url='https://sun9-84.userapi.com/impg/egjiF3q9pb-cvm-LS3bry7jF61_wflvH9BYxJQ/v8PKDBrOoBA.jpg?size=719x643&quality=95&sign=10b4e6f143c7231fe1e8c6d7749f4b1f&type=album',
            input_message_content = InputInvoiceMessageContent(
                title='Кепка подарок начинающему инвестору',
                description='легендарная кепка возвращается!\nТеперь можно заказать ее прямо в телеграме!\n ❗❗Доставка только по России❗❗',
                payload='kepo4ka',
                provider_token=PAYMENT_PROVIDER_TOKEN,
                currency='RUB',
                prices = [LabeledPrice('кепарик', 120000)],
                max_tip_amount=10050000,
                suggested_tip_amounts=[6000, 12000, 18000],
                # photo_size = 2,
                photo_height=719,
                photo_width=800,
                photo_url='https://sun9-84.userapi.com/impg/egjiF3q9pb-cvm-LS3bry7jF61_wflvH9BYxJQ/v8PKDBrOoBA.jpg?size=719x643&quality=95&sign=10b4e6f143c7231fe1e8c6d7749f4b1f&type=album',
                need_name=True,
                is_flexible=True,
                shipping_options=True,
                ),

        ),
    ]
    update.inline_query.answer(results)

def kepka_shipping(update: Update, context: CallbackContext) -> None:
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'kepo4ka':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message='Что-то пошло не так...')
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Почта России', [LabeledPrice('Почта России', 9000)]),
               ShippingOption('2', 'Почта России (экспресс)', [LabeledPrice('Почта России (экспресс)', 148800)]),
               ShippingOption('3', 'Самовывоз', [LabeledPrice('Самовывоз', 0)])]
    query.answer(ok=True, shipping_options=options)



def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "kepo4ka":
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)
        # send_message(update.effective_user.id, 'Спасибо за покупку')


def successful_payment_callback(update: Update, context: CallbackContext):
    shipping_options = {1: 'Почта России',
                        2: 'Почта России (экспресс)',
                        3: 'Самовывоз'}
    order_info = update.message.successful_payment.order_info.shipping_address
    full_address = f'{order_info.street_line1}, {order_info.street_line2}'
    city = order_info.city
    zip_code = order_info.post_code
    shipping_option = shipping_options[int(update.message.successful_payment.shipping_option_id)]
    print(full_address)
    print(city)
    print(zip_code)
    print(shipping_option)
    send_message(update.effective_user.id, 'Спасибо за покупку')



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern=r'1'))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(InlineQueryHandler(inline_query))
    dispatcher.add_handler(ShippingQueryHandler(kepka_shipping))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    # dispatcher.add_handler(MessageHandler(filters.successfu))
    # Run the bot until the user presses Ctrl-C
    updater.start_polling()


if __name__ == "__main__":
    main()
