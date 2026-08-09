from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.database import engine

def rooms_ids_for_booking(date_from, date_to, hotel_id: int | None = None):

        """
        with rooms_count as (
            select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        ),
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0;
        """

        

        rooms_count = (
        select(BookingsORM.room_id, func.count('*').label('rooms_booked'))
        .where(BookingsORM.date_from>=date_from, BookingsORM.date_to<=date_to)
        .group_by(BookingsORM.room_id)
        .cte(name='rooms_count')
        )

        rooms_left_table = (
            select(
                RoomsORM.id.label("room_id"),
                RoomsORM.hotel_id,
                (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsORM)
            .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        query = select(rooms_left_table.c.room_id).where(
        rooms_left_table.c.rooms_left > 0
        )

        # Опционально фильтруем по отелю
        if hotel_id is not None:
            query = query.where(rooms_left_table.c.hotel_id == hotel_id)
        
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return query