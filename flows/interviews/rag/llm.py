from langchain_openai import ChatOpenAI

# 나중에 환경변수로 변경.
def get_llm(model_name: str = "gpt-4o", temperature: float = 0.0):
    return ChatOpenAI(model_name=model_name, temperature=temperature)