import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import requests
import json
import time

# Загрузка переменных окружения из файла .env
load_dotenv('.env')

# Функция для отправки письма с новостями
def send_email_with_news(email, news_text):
    # Настройки почтового сервера и учетные данные
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = 'Новости'

    # Добавление текста новостей в сообщение
    body = news_text
    msg.attach(MIMEText(body, 'plain'))

    # Отправка письма
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    time.sleep(1)  # Пауза для завершения процесса шифрования
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, email, text)
    server.quit()

# Получение новостей с помощью API newsapi.org
def get_news(api_key):
    url = ('https://newsapi.org/v2/top-headlines?' 
           'sources=bbc-news&'
           'apiKey=' + api_key) 

    response = requests.get(url)
    data = response.json()

    # Проверка наличия ключа 'articles' в ответе
    if 'articles' not in data:
        print("Новости не найдены в ответе:", data)
        return ""

    # Извлечение заголовков новостей
    articles = data['articles']
    news_text = '\n\n'.join([f"{article['title']}\n{article['url']}" for article in articles])
    return news_text

def main(email) -> None:
    # Получение API ключа
    api_key = os.getenv('API_KEY')
   
    # Получение новостей
    news_text = get_news(api_key)

    # Отправка новостей по электронной почте
    send_email_with_news(email, news_text)

if __name__ == "__main__":
    main()
