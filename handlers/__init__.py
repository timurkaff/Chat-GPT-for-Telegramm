# handlers/__init__.py
def setup_handlers(bot, user_messages, user_message_ids):
    from .start import register_start_handler
    from .clear import register_clear_handler
    from .voice import register_voice_handler
    from .photo import register_photo_handler
    from .text import register_text_handler

    register_start_handler(bot, user_message_ids)
    register_clear_handler(bot, user_messages, user_message_ids)
    register_voice_handler(bot, user_messages, user_message_ids)
    register_photo_handler(bot, user_messages, user_message_ids)
    register_text_handler(bot, user_messages, user_message_ids)