# utils/ai.py
from duckduckgo_search import DDGS

def get_gpt_response(messages):
    prompt = messages[-1]['content'] 
    try:
        results = DDGS().chat(prompt, model='gpt-4o-mini')
        return results
    except Exception as e:
        return f"Ошибка запроса: {str(e)}"