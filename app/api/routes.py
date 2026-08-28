from fastapi import APIRouter, Header, HTTPException

from app.auth.authentication import get_current_user
from app.auth.authorization import require_permission
from app.models.users import USER_RECORDS

router = APIRouter()


def authenticate(authorization: str | None):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
        )

    token = authorization.replace("Bearer ", "")

    try:
        return get_current_user(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )


@router.get("/me")
def get_me(authorization: str | None = Header(default=None)):
    user = authenticate(authorization)

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    authorization: str | None = Header(default=None),
):
    user = authenticate(authorization)

    target = USER_RECORDS.get(user_id)

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

     # Object-level authorization:
    # Regular users can access only their own object.
    if user.role == "user" and user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user",
        )

    return {
       "requested_by": user.username,
        "user": {
            "id": target.id,
            "username": target.username,
            "email": target.email,
            "role": target.role,
        },
    }
