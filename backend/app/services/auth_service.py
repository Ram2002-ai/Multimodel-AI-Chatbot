"""Authentication business logic."""

from app.repositories.user import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, user_data: UserCreate) -> User:
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise UserAlreadyExistsException("User with this email already exists")
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
        )
        return await self.user_repo.create(user)

    async def authenticate(self, email: str, password: str) -> str:
        """Validate credentials and return an access token."""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Incorrect email or password")
        if not user.is_active:
            raise InvalidCredentialsException("Inactive user")
        return create_access_token(subject=user.id)

    async def get_user_by_token(self, token: str) -> User | None:
        from app.core.security import decode_access_token
        payload = decode_access_token(token)
        if payload is None:
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return await self.user_repo.get(user_id)