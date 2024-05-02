import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, String, create_engine
from smtp import main as send_news_email

# Загрузка переменных окружения из файла .env
load_dotenv('.env')

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Базовый класс для объявления моделей таблицы
Base = declarative_base()

# Класс модели таблицы для хранения адресов электронной почты
class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    telegram_user_id = Column(Integer)

# Создание движка базы данных SQLite
engine = create_engine('sqlite:///telega_bot.db', echo=True)

# Создание таблицы в базе данных
Base.metadata.create_all(engine)

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот новостей. Нажми /email, чтобы подписаться на новости.')

# Функция для обработки команды /email
def handle_email(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введите ваш электронный адрес:")
    context.user_data["waiting_for_email"] = True

# Функция для сохранения электронного адреса и отправки новостей
def save_email(update: Update, context: CallbackContext) -> None:
    email = update.message.text
    telegram_user_id = update.message.from_user.id
    context.user_data["email"] = email

    # Создание сессии для взаимодействия с базой данных
    Session = sessionmaker(bind=engine)

    # Использование контекстного менеджера sessionmaker
    with Session() as session:
        # Сохранение электронного адреса и id пользователя в базе данных
        new_email = Email(email=email, telegram_user_id=telegram_user_id)
        session.add(new_email)
        try:
            session.commit()
            update.message.reply_text("Я отправил новости на Ваш электронный адрес.")
            send_news_email(email)  # Отправка новостей по электронной почте
        except IntegrityError:
            session.rollback()
            update.message.reply_text("Спасибо что вернулись! Я отправил новости на Ваш электронный адрес.")
            send_news_email(email)  # Отправка новостей по электронной почте

def main() -> None:
    # Загрузка токена бота из переменной окружения
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Создание обработчика команд
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("email", handle_email))

    # Регистрация обработчика текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_email))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
