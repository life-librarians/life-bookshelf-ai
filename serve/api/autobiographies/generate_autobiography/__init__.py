import httpx
from fastapi import APIRouter

router = APIRouter()

# 자서전 생성 요청
async def save_autobiography(title, subtitle, autobiography, access_token: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://v2.lifebookshelf.org/main/api/v1/autobiographies",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "title": title,
                "subtitle": subtitle,
                "autobiography": autobiography
            },
            timeout=10.0
        )
