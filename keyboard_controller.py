from telegram import KeyboardButton, InlineKeyboardButton
from bd_control import bdcontroller


bd_unit = bdcontroller()


class KeyboardController():

    def main_menu():
        keyboard = [[
            InlineKeyboardButton('Новые заказы', callback_data='unsent_orders'),
            InlineKeyboardButton('', callback_data='unsent_orders'),
        ]]

        return keyboard

    # def continue_keyboard():
    #     keyboard = [[
    #         KeyboardButton('Продолжить', callback_data='1'),
    #     ]]
    #     return keyboard

    # def yes_no_keyboard():
    #     keyboard = [[
    #         KeyboardButton('Да', callback_data='Да'),
    #         KeyboardButton('Нет', callback_data='Нет'),
    #     ]]
    #     return keyboard

    # def lider_keyboard(liders:list):
    #     keyboard = [[
    #         KeyboardButton(f'{liders[0]}', callback_data=f'{liders[0]}'),
    #         KeyboardButton(f'{liders[1]}', callback_data=f'{liders[1]}')],
    #         [
    #         KeyboardButton(f'{liders[2]}', callback_data=f'{liders[2]}'),
    #         KeyboardButton(f'{liders[3]}', callback_data=f'{liders[3]}'),
    #     ]]
    #     return keyboard

    # def in_lider_keyboard(liders:list):
    #     keyboard = [[
    #         InlineKeyboardButton(f'{liders[0]}', callback_data=f'vote_{liders[0]}'),
    #         InlineKeyboardButton(f'{liders[1]}', callback_data=f'vote_{liders[1]}')],
    #         [
    #         InlineKeyboardButton(f'{liders[2]}', callback_data=f'vote_{liders[2]}'),
    #         InlineKeyboardButton(f'{liders[3]}', callback_data=f'vote_{liders[3]}'),
    #     ]]
    #     return keyboard

    # def in_continue_keyboard():
    #     keyboard = [[
    #         InlineKeyboardButton('Продолжить', callback_data='1'),
    #     ]]
    #     return keyboard


    # def in_yes_no_keyboard():
    #     keyboard = [[
    #         InlineKeyboardButton('Да', callback_data='notify_Да'),
    #         InlineKeyboardButton('Нет', callback_data='notify_Нет'),
    #     ]]
    #     return keyboard