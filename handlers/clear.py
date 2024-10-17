# handlers/clear.py
import telebot

def register_clear_handler(bot, user_messages, user_message_ids):
    @bot.message_handler(commands=['clear'])
    def clear_history(message):
        user_id = message.from_user.id

        # Очистка истории сообщений
        user_messages[user_id] = []

        # Удаление всех сообщений, связанных с текущим сеансом
        if user_id in user_message_ids:
            for msg_id in user_message_ids[user_id]:
                try:
                    bot.delete_message(message.chat.id, msg_id)
                except Exception as e:
                    print(f"Не удалось удалить сообщение {msg_id}: {e}")
            user_message_ids[user_id] = []

        # Уведомление об очистке истории
        confirmation_message = bot.send_message(message.chat.id, "История сообщений очищена.")

        if user_id not in user_message_ids:
            user_message_ids[user_id] = []

        user_message_ids[user_id].append(confirmation_message.message_id)
        user_message_ids[user_id].append(message.message_id)