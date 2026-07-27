from repos.base import BaseRepository
from src.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):

    model = RoomsORM