from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Register",
)
async def register(
    payload: RegisterRequest,
    usecase: AuthUseCase = Depends(get_auth_usecase),
) -> UserPublic:
    try:
        user = await usecase.register(email=payload.email, password=payload.password)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    return UserPublic.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase),
) -> TokenResponse:
    """Принимает форму OAuth2 (username = email)."""
    try:
        token = await usecase.login(email=form_data.username, password=form_data.password)
    except UnauthorizedError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return TokenResponse(access_token=token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Me",
)
async def me(
    user_id: int = Depends(get_current_user_id),
    usecase: AuthUseCase = Depends(get_auth_usecase),
) -> UserPublic:
    try:
        user = await usecase.get_profile(user_id=user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return UserPublic.model_validate(user)
