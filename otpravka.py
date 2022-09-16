from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()
PR_TOKEN = os.getenv('OTPRAVKA_TOKEN')
PR_KEY = os.getenv('OTPRAVKA_KEY')
# response = requests.get('https://website.example/id', headers={'Authorization': 'access_token myToken'})

class otpravka():
    load_dotenv()
    PR_TOKEN = os.getenv('OTPRAVKA_TOKEN')
    PR_KEY = os.getenv('OTPRAVKA_KEY')
    url = 'https://otpravka-api.pochta.ru/1.0/tariff'

 
    def get_price(self, index_from, index_to):
        file = open('tariff.json')
        data = json.load(file)
        headers = {
        'Authorization': f'AccessToken {PR_TOKEN}',
        'X-User-Authorization': f'Basic {PR_KEY}',
        'Content-Type': 'application/json;charset=UTF-8'
    }
        response = requests.post(self.url, headers=headers, json=data)
        print(response.json())


bibo = otpravka()
bibo.get_price(0, 0)