import os
from starlette.requests import Request

from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional, List

from constants import MemberRole
from logs import get_logger

logger = get_logger()

# 애플리케이션 및 시크릿 키 설정
app = FastAPI()
SECRET_KEY = os.environ.get("LIFE_BOOKSHELF_AI_JWT_SECRET_KEY")
ALGORITHM = "HS256"


class MemberSessionDto(BaseModel):
    member_id: int
    roles: List[MemberRole] = []


class AuthRequired(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization")
        logger.debug(f"Authorization header: {auth_header}")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_type, token = auth_header.split(" ")

        if token_type != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            request.state.token_info = verify_token(token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )


def verify_token(token: str) -> MemberSessionDto:
    try:
        logger.debug(f"Verifying token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded token payload: {payload}")
        member_id: int = payload.get("memberId")
        roles: List[MemberRole] = payload.get("roles") or []
        logger.debug(f"Member ID: {member_id}, Roles: {roles}")

        if member_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Member ID is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        member_session_dto = MemberSessionDto(member_id=member_id, roles=roles)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return member_session_dto


def get_current_user(request: Request) -> MemberSessionDto:
    return request.state.token_info
