from datetime import date

from fastapi import HTTPException

class EduFastApiException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(EduFastApiException):
    detail = "Объект не найден"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"    

class ObjectAlreadyExistsException(EduFastApiException):
    detail = "Похожий объект уже существует"    

class AllRoomsAreBookedException(EduFastApiException):
    detail = "Не осталось свободных номеров"

class UserExistsException(EduFastApiException):
    detail = "Пользователь с таким email уже существует"


class BookingDateException(EduFastApiException):
    detail = "Дата заезда не может быть больше или равной дате выезда"


class IncorrectTokenException(EduFastApiException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(EduFastApiException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(EduFastApiException):
    detail = "Пароль неверный"


class UserAlreadyExistsException(EduFastApiException):
    detail = "Пользователь уже существует"    

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from>=date_to:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда") 


class EduFastApiHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(EduFastApiHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(EduFastApiHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(EduFastApiHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(EduFastApiHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(EduFastApiHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(EduFastApiHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectPasswordHTTPException(EduFastApiHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(EduFastApiHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"               