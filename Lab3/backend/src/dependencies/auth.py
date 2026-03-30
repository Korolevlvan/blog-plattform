from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_token(token)
        return int(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials") from exc
