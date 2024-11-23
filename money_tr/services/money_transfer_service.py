class MoneyTransferService:
    def __init__(self):
        self.transactions = []

    def transfer(self, amount, currency): #имитируем денежный перевод
        transaction = {       #cоздаём словарь, представляющий одну транзакцию
            'amount': amount,
            'currency': currency
        }
        self.transactions.append(transaction)
        return f"Transfer of {amount} {currency} completed. Transaction recorded."