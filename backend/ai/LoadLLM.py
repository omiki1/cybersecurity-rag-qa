from langchain_openai import ChatOpenAI
import os

from pydantic import SecretStr

llm =None

def load_model():
    api_key = os.getenv('CHAT_OPENAI_API_KEY')
    global llm
    if not llm:
        llm = ChatOpenAI(
        api_key=SecretStr(api_key),
        base_url='https://api.deepseek.com',
        model='deepseek-v4-flash',
        streaming=True,
        temperature=0.5,
        top_p=1,
    )
        return llm
    else:
        return llm
