import pytest

from app.users.models import User
from app.users.repo import UserRepo


@pytest.mark.parametrize(
    "user_id, email, is_exists",
    [(1, "user@example.com", True), (10, "user@none.com", False)],
)
async def test_find_by_id(user_id, email, is_exists):
    user = await UserRepo.find_by_id(user_id)
    if is_exists:
        assert user is not None
        assert isinstance(user, User)
    else:
        assert user is None
