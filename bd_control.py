import psycopg2, os
from dotenv import load_dotenv
from datetime import datetime, timezone
dt = datetime.now()

load_dotenv()

class bdcontroller:
    conn = psycopg2.connect(database=os.getenv('db'), user=os.getenv('dbuser'),
                            password=os.getenv('dbpass'), host=os.getenv('host'), port=os.getenv('dbport'))
    # определение переменной для работы с запросами бд
    cur = conn.cursor()

    def create_order(self, full_address, index, full_name,
                     item_ordered, amount_charged,
                     customer_id, quantity, shipping_method, order_id, city, phone):
        self.cur.execute(f"INSERT INTO orders(full_address, index, full_name, item_ordered, amount_charged, order_status, customer_id, quantity, shipping_method, order_id, city, phone_number) VALUES ('{full_address}', {index}, '{full_name}', '{item_ordered}', {amount_charged}, 'Принят', {customer_id}, {quantity}, {shipping_method}, {order_id}, {city}, {phone});")
        self.conn.commit()

    def generate_order_id(self):
        self.cur.execute('SELECT COUNT(*) FROM orders GO')
        id = self.cur.fetchone()
        return(id[0] + 1)


    def get_all_unsent_orders(self):
        self.cur.execute('SELECT COUNT(*) FROM orders WHERE shipped_out=False')
        return(self.cur.fetchone()[0])


    def get_x_last_unsent_orders(self, limit):
        self.cur.execute(f'SELECT order_id, full_name, full_address, index FROM orders WHERE shipped_out=False ORDER BY order_date DESC LIMIT {limit}')
        return(self.cur.fetchall())

    def get_order_info(self, order_id):
        self.cur.execute(f'SELECT city, full_address, index, full_name, shipping_method, item_ordered, quantity FROM orders WHERE order_id = {order_id}')
        return(self.cur.fetchone())

    def set_shipped_out(self, order_id, flag):
        self.cur.execute(f'UPDATE orders SET shipped_out = {flag} WHERE order_id = {order_id}')
        self.conn.commit()
        return(f'поменяли заказ №{order_id} на {flag}')

    def check_sent(self, order_id):
        self.cur.execute(f'SELECT shipped_out FROM orders WHERE order_id = {order_id}')
        self.conn.commit()
        return self.cur.fetchone()[0]


# biba = bdcontroller()
# print(biba.check_sent(1)[0])

# biba.create_order(
#     'adress',
#     12312,
#     'vasya pupkin',
#     'kepka',
#     100.99,
#     1111122222,
#     1
# )
