from abc import ABC

from core.models import User, UserExtended
from core.repositories.abc_meta import RepoMeta


class UserRepo(RepoMeta[User, UserExtended, int], ABC):
    pass
