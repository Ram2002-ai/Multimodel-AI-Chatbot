import pytest
from app.models.user import User
from app.repositories.user import UserRepository

@pytest.mark.asyncio
async def test_create_user(async_session):
    repo = UserRepository(async_session)
    user = User(email="test@example.com", hashed_password="hashed", full_name="Test")
    saved = await repo.create(user)
    assert saved.id is not None
    fetched = await repo.get_by_email("test@example.com")
    assert fetched is not None
    assert fetched.full_name == "Test"