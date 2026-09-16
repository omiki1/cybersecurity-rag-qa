from langchain_openai import ChatOpenAI
import os

from pydantic import SecretStr

llm = None

def load_model():
    api_key = os.getenv('GLM_API_KEY')
    global llm
    if not llm:
        llm = ChatOpenAI(
            api_key=SecretStr(api_key),
            base_url='https://open.bigmodel.cn/api/paas/v4/',
            model='glm-4.5-air',
            streaming=True,
            temperature=0.5,
            top_p=1,
        )
        return llm
    else:
        return llm
