from services.valute_converter_service import ValuteConverterService
from services.money_transfer_service import MoneyTransferService
from services.notification_service import NotificationService

class CentralService:
    def __init__(self):
        self.converter = ValuteConverterService()
        self.money_transfer_service = MoneyTransferService()
        self.notification_service = NotificationService()

    def initiate_transfer(self, user, amount, from_currency, to_currency, comment=""):
        try:
            converted_amount = self.converter.convert(amount, from_currency, to_currency)
            transaction_result = self.money_transfer_service.transfer(converted_amount, to_currency)

            self.notification_service.notify(user, converted_amount, to_currency, comment)
            return transaction_result
        except Exception as e:
            print(f"Ошибка во время перевода: {e}")
            return f"Ошибка перевода: {e}"