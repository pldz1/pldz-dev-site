from fastapi import HTTPException, status

from scripts.db import AuthorizedHandler


def ensure_authenticated(
    user: dict,
    *,
    detail: str,
    status_code: int = status.HTTP_401_UNAUTHORIZED,
) -> dict:
    if not user:
        raise HTTPException(status_code=status_code, detail=detail)
    return user


def ensure_admin_user(
    user: dict,
    *,
    login_detail: str,
    forbidden_detail: str,
) -> dict:
    current_user = ensure_authenticated(user, detail=login_detail)
    if not AuthorizedHandler.check_admin(current_user.get("username")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=forbidden_detail,
        )
    return current_user
