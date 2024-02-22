from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.blacklisted_token import BlacklistedToken
from app.repository.base_repository import BaseRepository


class BlacklistedTokenRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, BlacklistedToken)
