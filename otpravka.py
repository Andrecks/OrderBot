from dotenv import load_dotenv
import os
import requests
import json
from retry import retry

load_dotenv()
PR_TOKEN = os.getenv('OTPRAVKA_TOKEN')
PR_KEY = os.getenv('OTPRAVKA_KEY')
# response = requests.get('https://website.example/id', headers={'Authorization': 'access_token myToken'})

class otpravka():
    load_dotenv()
    PR_TOKEN = os.getenv('OTPRAVKA_TOKEN')
    PR_KEY = os.getenv('OTPRAVKA_KEY')
    url = 'https://otpravka-api.pochta.ru/1.0/tariff'
    headers = {
        'Authorization': f'AccessToken {PR_TOKEN}',
        'X-User-Authorization': f'Basic {PR_KEY}',
        'Content-Type': 'application/json;charset=UTF-8'
    }

    @retry(tries=5, delay=1)
    def get_price(self, index_to):
        file = open('tariff.json')
        data = json.load(file)
        data['index-to'] = index_to
        print(data)
        response = requests.post(self.url, headers=self.headers, json=data).json()
        return (self.plural_days(response['delivery-time']['max-days'] + 2), response['total-rate'])

    def plural_days(self, n):
        days = ['день', 'дня', 'дней']
        if n % 10 == 1 and n % 100 != 11:
            p = 0
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            p = 1
        else:
            p = 2

        return str(n) + ' ' + days[p]

    def create_order(self, name, surname):
        pass
# bibo = otpravka()
# # try:
# print(bibo.get_price('117342'))
# # except:
# #     print('fail')
