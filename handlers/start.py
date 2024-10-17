# handlers/start.py
import telebot

def register_start_handler(bot, user_message_ids):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user_id = message.from_user.id

        # Инициализация списка сообщений и их идентификаторов для нового пользователя
        if user_id not in user_message_ids:
            user_message_ids[user_id] = []

        bot_message = bot.send_message(
            message.chat.id,
            "Привет! Я ваш AI помощник. Используйте команду /clear для очистки истории сообщений."
        )
        user_message_ids[user_id].append(bot_message.message_id)
        user_message_ids[user_id].append(message.message_id)