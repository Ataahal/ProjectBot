import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import time
import json

# Загрузка переменных окружения из файла .env
load_dotenv('.env')

# Функция для отправки письма с новостями
# def send_email_with_news(news_text):
#     # Настройки почтового сервера и учетные данные
#     SMTP_SERVER = "smtp-relay.gmail.com"
#     SMTP_PORT = 587
#     EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
#     EMAIL_ADDRESS2 = os.getenv('EMAIL_ADDRESS2')
#     EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

#     # Создание сообщения
#     msg = MIMEMultipart()
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = EMAIL_ADDRESS2
#     msg['Subject'] = 'Новости'

#     # Добавление текста новостей в сообщение
#     body = news_text
#     msg.attach(MIMEText(body, 'plain'))

#     # Отправка письма
#     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#     server.starttls()
#     time.sleep(1)  # Пауза для завершения процесса шифрования
#     server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#     text = msg.as_string()
#     server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS2, text)
#     server.quit()

# Получение новостей с помощью API newsapi.org
def get_news(api_key):
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=us&'
           'apiKey=' + api_key) 

    response = requests.get(url)
    data = response.json()
    with open("my.json", "w") as file:
        json.dump(data, file, indent=2)

    # Проверка наличия ключа 'articles' в ответе
    if 'articles' not in data:
        print("Новости не найдены в ответе:", data)
        return ""

    # Извлечение заголовков новостей
    articles = data['articles']
    news_text = '\n\n'.join([f"{article['title']}\n{article['url']}" for article in articles])
    return news_text

def main():
    # Получение API ключа
    api_key = os.getenv('API_KEY')
   
    # Получение новостей
    news_text = get_news(api_key)

    # # Отправка новостей по электронной почте
    # send_email_with_news(news_text)

if __name__ == "__main__":
    main()
