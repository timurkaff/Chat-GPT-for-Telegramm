# handlers/text.py
import telebot
from utils.ai import get_gpt_response
from utils.formatting import format_code

def register_text_handler(bot, user_messages, user_message_ids):
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_id = message.from_user.id

        # Инициализация, если необходимо
        if user_id not in user_messages:
            user_messages[user_id] = []
        if user_id not in user_message_ids:
            user_message_ids[user_id] = []

        # Сохранение ID сообщения
        user_message_ids[user_id].append(message.message_id)

        # Если сообщение является командой, не обрабатываем его как текстовое сообщение
        if message.text.startswith('/'):
            return

        # Добавление сообщения пользователя в список
        user_messages[user_id].append({'role': 'user', 'content': message.text})

        # Установить статус "typing"
        bot.send_chat_action(message.chat.id, 'typing')

        # Получение ответа от AI
        gpt_response = get_gpt_response(user_messages[user_id])

        # Форматирование ответа, если он содержит код
        formatted_response = format_code(gpt_response)

        # Добавление ответа AI в список сообщений
        user_messages[user_id].append({'role': 'assistant', 'content': formatted_response})

        # Установить статус "typing"
        bot.send_chat_action(message.chat.id, 'typing')

        # Отправка ответа пользователю
        sent_message = bot.send_message(message.chat.id, formatted_response, parse_mode="HTML")
        user_message_ids[user_id].append(sent_message.message_id)