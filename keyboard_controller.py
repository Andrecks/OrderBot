from telegram import KeyboardButton, InlineKeyboardButton
from bd_control import bdcontroller


bd_unit = bdcontroller()


class KeyboardController():

    def admin_main(self):
        keyboard = [[
            InlineKeyboardButton('Новые заказы', callback_data='unsent_page#1'),
        ]]

        return keyboard

    def generate_text_for_order(self, order):
        return(f'заказ №{order[0]}\nимя: {order[1]}')

    def generate_full_order(self, order_id):
        order_details = bd_unit.get_order_info(order_id)
        print(f'ORDER DETAILS HERE: {order_details}')
        return(f'Город: {order_details[0]}\nАдрес: {order_details[1]}\n'
        f'Индекс: {order_details[2]}\n'
        f'Имя: {order_details[3]}\n'
        f'Способ доставки: {order_details[4]}\n'
        f'Товар: {order_details[5]}\n'
        f'Количество: {order_details[6]}\n')


    def admin_order_info(self, order_id):
        keyboard = [
            [InlineKeyboardButton('создать отправление', callback_data=f'create_otpravka#{order_id}')],
            [InlineKeyboardButton('отметить как неотправленный', callback_data=f'shipped_out#{order_id}#False')],
            [InlineKeyboardButton('вернуться к новым заказам', callback_data=f'unsent_page#1')],
            [InlineKeyboardButton('завершить сессию', callback_data=f'close_session')]]
        if not bd_unit.check_sent(order_id):
            return(keyboard)
        else:
            keyboard[0] = [InlineKeyboardButton('отметить как отправленный', callback_data=f'shipped_out#{order_id}#True')]

    def build_orders_keyboard(self, orders):
        keyboard = []
        for order in orders:
            keyboard.append([InlineKeyboardButton(text=self.generate_text_for_order(order), callback_data=f'order#{order[0]}')])
        keyboard.append([InlineKeyboardButton('завершить сессию', callback_data=f'close_session')])
        return keyboard

    # def get_orders_for_page(self, page, max_page, order_count, order_per_page):
    #     if page >= max_page:
    #         limit = order_count%order_per_page
    #         if limit != 0:
    #             orders = bd_unit.get_x_last_unsent_orders(limit)
    #             return(self.build_orders_keyboard(orders))
        #TODO: добавить пагинацию страниц кроме последней


