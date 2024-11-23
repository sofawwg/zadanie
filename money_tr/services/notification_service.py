import redis
import sqlite3
from datetime import datetime
import threading


class NotificationService:
    def __init__(self, db_name='transactions.db'):
        self.db_name = db_name
        self.local = threading.local() #бд

        #редис
        self.redis_client = redis.StrictRedis(host='127.0.0.1', port='6379', decode_responses=True)

    def _get_connection(self): #соединение с бд
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_name)
            self.local.cursor = self.local.connection.cursor()
            self._create_table()
        return self.local.connection, self.local.cursor

    def _create_table(self):
        connection, cursor = self._get_connection()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                comment TEXT,
                date TEXT NOT NULL
            )
        ''')
        connection.commit()


    def notify(self, user, amount, currency, comment): #уведомление через Redis
        connection, cursor = self._get_connection()
        try:
            message = f"Уведомление о переводе для: {user} - {amount} {currency} ({comment})"
            self.redis_client.publish('notifications', message)
            print(f"Сообщение '{message}' отправлено через Redis")
            self.record_transaction(user, amount, currency, comment, cursor, connection)
        except redis.RedisError as e:
            print(f"Ошибка отправки сообщения через Redis: {e}")

    def record_transaction(self, user, amount, currency, comment, cursor, connection):
        cursor.execute('''
            INSERT INTO transactions (user, amount, currency, comment, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user, amount, currency, comment, datetime.now().isoformat()))
        connection.commit()


    def close(self):
        if hasattr(self.local, 'connection'):
            self.local.connection.close()