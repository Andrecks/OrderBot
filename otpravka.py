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

 
    def get_price(self, full_adress, index):
        file = open('tariff.json')
        data = json.load(file)
        headers = {
        'Authorization': 'AccessToken 94EgbSPrglChjiZtmY7it2iSjJXP6ZN3',
        'X-User-Authorization': 'Basic Kzc5MTY2NDc3OTU0Omdvb2dpbjMyMQ==',
        'Content-Type': 'application/json;charset=UTF-8'
    }
        response = requests.post(self.url, headers=headers, json=data)
        print(response.json())


bibo = otpravka()
bibo.get_price(0, 0)