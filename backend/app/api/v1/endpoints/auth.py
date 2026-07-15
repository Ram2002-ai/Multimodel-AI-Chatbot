from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService
from app.api.deps import get_auth_service, get_current_active_user
from app.models.user import User
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = await auth_service.register(user_in)
        return user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = await auth_service.authenticate(login_data.email, login_data.password)
        return TokenResponse(access_token=token)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user