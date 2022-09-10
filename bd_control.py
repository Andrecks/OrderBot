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
                     customer_id, quantity, shipping_method, order_id, city):
        self.cur.execute(f"INSERT INTO orders(full_address, index, full_name, item_ordered, amount_charged, order_status, customer_id, quantity, shipping_method, order_id, city) VALUES ('{full_address}', {index}, '{full_name}', '{item_ordered}', {amount_charged}, 'Принят', {customer_id}, {quantity}, {shipping_method}, {order_id}, {city});")
        self.conn.commit()

    def generate_order_id(self):
        self.cur.execute('SELECT COUNT(*) FROM orders GO')
        id = self.cur.fetchone()
        return(id[0])


# biba = bdcontroller()
# biba.generate_order_id()

# biba.create_order(
#     'adress',
#     12312,
#     'vasya pupkin',
#     'kepka',
#     100.99,
#     1111122222,
#     1
# )
