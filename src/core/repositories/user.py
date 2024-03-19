from abc import ABC

from core.models import User
from core.repositories.abc import RepoMeta


class UserRepo(RepoMeta[User, User, int], ABC):
    pass
