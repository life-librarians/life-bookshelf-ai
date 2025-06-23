import httpx
from logs import get_logger

logger = get_logger()

# 질문과 답변 데이터 저장
async def save_qa_to_main_server(question, answer, access_token: str):
    async with httpx.AsyncClient() as client:
        # Question (BOT)
        await client.post(
            "https://v2.lifebookshelf.org/main/api/v1/interviews/conversations",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "conversations": [
                    {
                        "content": question,
                        "conversationType": "BOT"
                    }
                ]
            },
            timeout=5.0
        )

        # Answer (HUMAN)
        await client.post(
            "https://v2.lifebookshelf.org/main/api/v1/interviews/conversations",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "conversations": [
                    {
                        "content": answer,
                        "conversationType": "HUMAN"
                    }
                ]
            },
            timeout=5.0
        )

# 최신 sub topic 업데이트
async def update_current_subtopic(title, subtitle, subtopic, access_token: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://v2.lifebookshelf.org/main/api/v1/interviews/current-chapter",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "title": title,
                "subtitle": subtitle,
                "subtopic": subtopic
            },
            timeout=3.0
        )