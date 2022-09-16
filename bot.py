import os

from dotenv import load_dotenv
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                      InlineQueryResult, InlineQueryResultArticle, InlineQueryResultVoice, InputMediaPhoto,
                      InputTextMessageContent, Invoice, MenuButton,
                      ReplyKeyboardRemove, ReplyMarkup, SuccessfulPayment, Update, LabeledPrice, InputInvoiceMessageContent, ShippingOption)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, InlineQueryHandler, Updater,
                          ShippingQueryHandler, PreCheckoutQueryHandler, MessageHandler,
                          Filters, callbackqueryhandler)
from telegram_bot_pagination import InlineKeyboardPaginator
from bd_control import bdcontroller
from keyboard_controller import KeyboardController

kb_unit = KeyboardController()
bd_unit = bdcontroller()
load_dotenv()

# добавляем админов по айди из .env
# amdins = 123456789 123456789
ADMINS = os.getenv('admins').split()

# Токен проавдейра
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')
bot = Bot(token=os.getenv('TOKEN'))
updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher
items_for_order = {'kepo4ka': ['Кепка долбаеб', 1]}
shipping_options = {1: 'Почта России',
                    2: 'Почта России (экспресс)',
                    3: 'Самовывоз'}


ORDERS_PER_PAGE = 5  #  количество отображаемых заказов на странице в админке


def start(update: Update, context: CallbackContext) -> None:
    pass

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


def inline_query(update: Update, context: CallbackContext) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    results = [
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
                need_shipping_address=True,
                need_phone_number=True,
                ),

        ),
    ]
    update.inline_query.answer(results)

def kepka_shipping(update: Update, context: CallbackContext) -> None:
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    country_code = query.shipping_address.country_code
    # check the payload, is this from your bot?
    if (query.invoice_payload != 'kepo4ka') or country_code != 'RU':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message='Что-то пошло не так...')
        return
    print(f'SHIPPING HERE {query}')
    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Почта России', [LabeledPrice('Почта России', 9000)]),
            #    ShippingOption('2', 'Почта России (экспресс)', [LabeledPrice('Почта России (экспресс)', 148800)]),
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
        #TODO: Запилить проверку курьерской доставки по Мск
        query.answer(ok=True)


def successful_payment_callback(update: Update, context: CallbackContext):
    full_update = update.message.successful_payment
    order_info = full_update.order_info
    shipping_info = full_update.order_info.shipping_address
    full_address = f'{shipping_info.street_line1}, {shipping_info.street_line2}'
    items_ordered = items_for_order[full_update.invoice_payload]
    sum_charged = f'{int(full_update.total_amount/100)}.{str(full_update.total_amount)[-2:]}'
    # print(f'AFTER PAY {update.message.successful_payment}')
    # print('--------')
    zip_code = shipping_info.post_code
    shipping_option = shipping_options[int(update.message.successful_payment.shipping_option_id)]
    bd_unit.create_order(full_address, zip_code, order_info.name,
                         items_ordered[0], sum_charged, update.message.from_user.id,
                         items_ordered[1], f"'{shipping_options[int(full_update.shipping_option_id)]}'",
                         bd_unit.generate_order_id(), f"'{shipping_info.city}'",
                         phone_number)
    send_message(update.effective_user.id, 'Спасибо за покупку')


def admin_login(update: Update, context: CallbackContext):
    # update.callback_query.answer()
    user_id = update.message.from_user.id
    if str(user_id) in ADMINS:
        update.message.delete()
        send_message(user_id, 'добро пожаловать в админку',
        reply_markup=InlineKeyboardMarkup(kb_unit.admin_main()))


def admin_new_orders(update: Update, context: CallbackContext):

    user_id = update.effective_user.id
    query =  update.callback_query
   
    # query.answer()
    if str(user_id) in ADMINS:
        update.callback_query.delete_message()

        page = int(query.data.split('#')[1])
        unsent_orders_count = bd_unit.get_all_unsent_orders()
        MAX_PAGES = unsent_orders_count // ORDERS_PER_PAGE + 1
        # пагинатор в ифе, можно от него избавиться
        if unsent_orders_count > ORDERS_PER_PAGE:
            paginator = InlineKeyboardPaginator(
            MAX_PAGES,  # формула подсчета пагинатора
            current_page=page,
            data_pattern='unsent_page#{page}'
        )
            paginator.add_before(kb_unit.get_orders_for_page(page, MAX_PAGES, unsent_orders_count, ORDERS_PER_PAGE))
        else:

            reply_markup = InlineKeyboardMarkup(kb_unit.build_orders_keyboard(bd_unit.get_x_last_unsent_orders(limit=unsent_orders_count)))
            send_message(user_id, f'всего новых заказов: {bd_unit.get_all_unsent_orders()}',
                     reply_markup=reply_markup)

def get_full_order_info(update: Update, context: CallbackContext):
    
    user_id = update.effective_user.id
    query =  update.callback_query
    
    if str(user_id) in ADMINS:
        update.callback_query.delete_message()
        order_id = int(query.data.split('#')[1])
        send_message(user_id, kb_unit.generate_full_order(order_id),
                     reply_markup=InlineKeyboardMarkup(kb_unit.admin_order_info(order_id)))

def set_order_shipped_out(update: Update, context: CallbackContext):

    query =  update.callback_query
    user_id = update.effective_user.id
 
    if str(user_id) in ADMINS:
        order_id = int(query.data.split('#')[1])
        shipped_flag = query.data.split('#')[2]
        reply_markup = InlineKeyboardMarkup(kb_unit.admin_order_info(order_id))
        if shipped_flag == 'True':
            bd_unit.set_shipped_out(order_id, shipped_flag)
            update.callback_query.edit_message_text(f'заказ #{order_id} отмечен как отправленный', reply_markup=reply_markup)
        else:
            bd_unit.set_shipped_out(order_id, shipped_flag)
            update.callback_query.edit_message_text(f'заказ #{order_id} отмечен как неотправленный', reply_markup=reply_markup)

def close_session(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if str(user_id) in ADMINS:
        update.callback_query.edit_message_reply_markup(reply_markup=None)

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
    dispatcher.add_handler(CommandHandler("admin", admin_login))
    dispatcher.add_handler(CallbackQueryHandler(admin_new_orders, pattern=r'unsent_page#'))  # paginator
    dispatcher.add_handler(CallbackQueryHandler(get_full_order_info, pattern=r'order#'))
    dispatcher.add_handler(CallbackQueryHandler(set_order_shipped_out, pattern=r'shipped_out#'))
    dispatcher.add_handler(CallbackQueryHandler(close_session, pattern=r'close_session'))
    # dispatcher.add_handler(MessageHandler(filters.successfu))
    # Run the bot until the user presses Ctrl-C
    updater.start_polling()


if __name__ == "__main__":
    main()
