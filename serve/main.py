import os

from fastapi import FastAPI
from promptflow.connections import AzureOpenAIConnection, OpenAIConnection
from promptflow.client import PFClient
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from autobiographies.generate_autobiography.router import (
    router as autobiographies_generate_autobiography_router,
)
from chapters.generate_chapter.router import (
    router as autobiographies_generate_chapter_router,
)
from interviews.interview_chat.router import (
    router as interviews_request_interview_chat_router,
)

from logs import get_logger

load_dotenv(dotenv_path=".env.development")

logger = get_logger()


def create_connection():
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    connection = None
    if api_key.startswith("sk-"):
        connection = OpenAIConnection(
            name="open_ai_connection",
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        )
    else:
        connection = AzureOpenAIConnection(
            name="open_ai_connection",
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_base=os.environ.get("AZURE_OPENAI_API_BASE"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_API_BASE", "azure"),
            api_version=os.environ.get(
                "AZURE_OPENAI_API_VERSION", "2023-07-01-preview"
            ),
        )

    pf = PFClient()
    conn = pf.connections.create_or_update(connection)

    logger.info(f"Successfully created connection {conn}")


create_connection()


app = FastAPI(
    description="Life Bookshelf AI API",
    version="0.0.1",
    docs_url="/docs",
    root_path="/ai"
)

origins = [
    "http://localhost:8080",  # MagicMirror 클라이언트 주소
    "http://127.0.0.1:8080",
    "http://10.165.145.241:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["*"]로 전체 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autobiographies_generate_autobiography_router)
app.include_router(autobiographies_generate_chapter_router)
app.include_router(interviews_request_interview_chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
