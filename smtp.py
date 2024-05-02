import os
import requests
import smtplib
import time
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Загрузка переменных окружения из файла .env
load_dotenv('.env')


def send_email_with_news(email, news_text):
    """Отправляет письмо с новостями на указанный адрес электронной почты."""
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
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        time.sleep(1)  # Пауза для завершения процесса шифрования
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, email, text)


def get_news(api_key):
    """Получает новости с помощью API newsapi.org."""
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
    """Отправляет новости по указанному адресу электронной почты."""
    # Получение API ключа
    api_key = os.getenv('API_KEY')

    # Получение новостей
    news_text = get_news(api_key)

    # Отправка новостей по электронной почте
    send_email_with_news(email, news_text)


if __name__ == "__main__":
    main()
