import os

from fastapi import FastAPI
from promptflow.connections import AzureOpenAIConnection, OpenAIConnection
from promptflow.client import PFClient
from dotenv import load_dotenv

from autobiographies.generate_autobiography.router import (
    router as autobiographies_generate_autobiography_router,
)
from autobiographies.generate_correction.router import (
    router as autobiographies_generate_correction_router,
)
from chapters.generate_chapter.router import (
    router as autobiographies_generate_chapter_router,
)
from interviews.generate_interview_question.router import (
    router as interviews_generate_interview_question_router,
)
from interviews.interview_chat.router import (
    router as interviews_request_interview_chat_router,
)

from logs import get_logger

load_dotenv()

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
)

app.include_router(autobiographies_generate_autobiography_router)
app.include_router(autobiographies_generate_correction_router)
app.include_router(autobiographies_generate_chapter_router)
app.include_router(interviews_generate_interview_question_router)
app.include_router(interviews_request_interview_chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
