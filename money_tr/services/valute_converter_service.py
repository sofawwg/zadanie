import requests
import time


class ValuteConverterService:
    API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'  #возвращает обменные курсы

    def __init__(self):
        self.last_updated = 0
        self.rates = {}

    def update_rates(self):   #последние курсы обмена из API
        response = requests.get(self.API_URL)
        if response.status_code == 200:
            data = response.json()
            self.rates = data['rates']
            self.last_updated = time.time()

    def convert(self, amount, from_currency, to_currency):
        if time.time() - self.last_updated > 14400:  #обновляем каждые 4 часа
            self.update_rates()

        if from_currency != 'USD':  #tсли from_currency не является долларом, сначала конвертируется сумма в доллары путём деления на обменный курс
            amount /= self.rates[from_currency]

        return amount * self.rates[to_currency]