# handlers/photo.py
import telebot
import os
from PIL import Image
import pytesseract
from utils.ai import get_gpt_response
from utils.formatting import format_code

def register_photo_handler(bot, user_messages, user_message_ids):
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        user_id = message.from_user.id

        # Инициализация, если необходимо
        if user_id not in user_messages:
            user_messages[user_id] = []
        if user_id not in user_message_ids:
            user_message_ids[user_id] = []

        # Получение файла изображения
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохранение изображения
        photo_path = f"photo_{user_id}.jpg"
        with open(photo_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Открытие изображения и распознавание текста
        image = Image.open(photo_path)
        text = pytesseract.image_to_string(image, lang='rus')

        # Удаление временного файла
        os.remove(photo_path)

        # Сохранение ID сообщения
        user_message_ids[user_id].append(message.message_id)

        # Добавление сообщения пользователя в список
        user_messages[user_id].append({'role': 'user', 'content': text})

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