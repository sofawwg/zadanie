import redis
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class RedisSubscriber:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0, sender_email="sofiarolzina@mail.ru", receiver_email="fedor.rolzin@mail.ru", password="XgWfNgTnUCcSRzEgBrCR"):
      self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
      self.channel = 'transfer_notifications'
      self.sender_email = sender_email
      self.receiver_email = receiver_email
      self.password = password

    def run(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.channel)
        for message in pubsub.listen():
            if message['type'] == 'message':
                self.send_email(message['data'].decode('utf-8'))

    def send_email(self, message):
        msg = MIMEMultipart()
        msg['Subject'] = 'Уведомление о переводе'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg.attach(MIMEText(message))

        try:
            with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
        except smtplib.SMTPException as e:
            print(f"Ошибка отправки email: {e}")