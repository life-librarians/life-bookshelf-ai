import httpx
from logs import get_logger

logger = get_logger()

async def save_qa_to_main_server(title, subtitle, subtopic, question, answer, access_token: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://main-server.internal/api/v1/interviews/save-qa",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "title": title,
                "subtitle": subtitle,
                "subtopic": subtopic,
                "question": question,
                "answer": answer
            },
            timeout=5.0
        )

async def update_current_subtopic(title, subtitle, subtopic, access_token: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://main-server.internal/api/v1/interviews/current-subtopic",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "title": title,
                "subtitle": subtitle,
                "subtopic": subtopic
            },
            timeout=3.0
        )

async def trigger_autobiography_generation(title, subtitle, chapters, access_token: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://ai-server.internal:3000/generate-autobiography",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "title": title,
                "subtitle": subtitle,
                "chapters": chapters
            },
            timeout=10.0
        )
