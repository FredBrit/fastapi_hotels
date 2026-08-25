
class EduFastApiException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(EduFastApiException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(EduFastApiException):
    detail = "Не осталось свободных номеров"
