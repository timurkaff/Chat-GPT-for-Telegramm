# utils/formatting.py
import re

def format_code(message):
    # Шаблон для поиска всех кодовых блоков
    code_block_pattern = re.compile(r'```(?:\w+)?\n(.*?)```', re.DOTALL)
    
    def replace_code_block(match):
        code = match.group(1)
        # Заменяем символы < и > на их HTML-сущности, чтобы избежать проблем с парсингом
        code = code.replace('<', '&lt;').replace('>', '&gt;')
        return f"<pre>{code}</pre>"

    # Заменяем все кодовые блоки в сообщении
    formatted_message = code_block_pattern.sub(replace_code_block, message)
    
    return formatted_message