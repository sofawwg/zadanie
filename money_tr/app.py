from flask import Flask, render_template, request, redirect, url_for
from services.central_service import CentralService
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

central_service = CentralService() #создаём экземпляр класса который обрабатывает фактические операции по переводу денег

@app.route('/')
def index(): #обрабатывает запросы к корневому URL
    return render_template('index.html')

@app.route('/transfer', methods=['POST']) #POST-запросы к /transfer
def transfer():
    try:
        #получаем данные
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency'].upper()
        to_currency = request.form['to_currency'].upper()
        user = request.form.get('user')
        comment = request.form.get('comment', '')

        if not user:
          return render_template('index.html', error="User information missing") #обработка отсутствующего пользователя


        #проверка верности данных
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if not from_currency or not to_currency:
            raise ValueError("Currencies are required.")

        transaction_result = central_service.initiate_transfer(user, amount, from_currency, to_currency, comment)

        if "completed" in transaction_result:
          logging.info(f"Successful transfer: {transaction_result}")
          return redirect(url_for('success'))  #если перевод выполнен, то перекидываемна стр успешного выполнения

        else:
          logging.error(f"Transfer failed: {transaction_result}") #если передача неудачная
          return render_template('index.html', error=transaction_result)

    except ValueError as e:
        logging.error(f"Validation error: {e}")
        return render_template('index.html', error=str(e))
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return render_template('index.html', error="An unexpected error occurred. Please try again later.")


@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)