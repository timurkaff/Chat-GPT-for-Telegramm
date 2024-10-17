# handlers/voice.py
import telebot
import os
import speech_recognition as sr
from pydub import AudioSegment
from utils.ai import get_gpt_response
from utils.formatting import format_code

def register_voice_handler(bot, user_messages, user_message_ids):
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        user_id = message.from_user.id

        # Скачивание голосового сообщения
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохранение голосового сообщения как .ogg файл
        ogg_path = f"voice_{user_id}.ogg"
        wav_path = f"voice_{user_id}.wav"
        with open(ogg_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Конвертация .ogg файла в .wav формат
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format='wav')

        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(wav_path)

        try:
            with audio_file as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='ru-RU')
        except sr.UnknownValueError:
            text = "Извините, не удалось распознать аудио."
        except sr.RequestError:
            text = "Ошибка при запросе к сервису распознавания."

        # Удаление временных файлов
        os.remove(ogg_path)
        os.remove(wav_path)

        # Инициализация, если необходимо
        if user_id not in user_messages:
            user_messages[user_id] = []
        if user_id not in user_message_ids:
            user_message_ids[user_id] = []

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