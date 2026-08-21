from sqlalchemy import select, insert, update
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.schemas.bookings import Booking, BookingAdd
from src.repos.mappers.mappers import BookingDataMapper



class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper


    async def add_booking(
        self,
        data: BookingAdd
        ):
    
        room_check = await self.session.execute(
            select(RoomsORM.quantity).where(RoomsORM.id == data.room_id)
        )
        available_quantity = room_check.scalar()
        print(f'Количество комнат: {available_quantity}')

        if not available_quantity or available_quantity == 0:
            raise ValueError(f'У номера {data.room_id} нет свободных мест')

        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)

        update_quantity = (
            update(RoomsORM)
            # Добавляем проверку, что количество больше 0
            .where(RoomsORM.id == data.room_id, RoomsORM.quantity > 0) 
            .values(quantity=RoomsORM.quantity - 1)
        )
        result2 = await self.session.execute(update_quantity)

        
        # Возвращаем первый (и единственный) созданный объект, пропущенный через маппер
        created_booking = result.scalar_one()
        return self.mapper.map_to_domain_entity(created_booking)   
