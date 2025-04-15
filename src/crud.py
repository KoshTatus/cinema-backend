from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from starlette import status

from src.models import MoviesOrm, GenresOrm, OrdersOrm, MovieGenresOrm, HallsOrm, SessionsOrm, SeatsOrm, UsersOrm
from src.schemas import Movie, Genre, Order, OrderCreate, Hall, Session as SessionSchema, SessionDetailed, Seat, \
    OrderDetailed, User, UserWithOrders


def get_all_movies(
        db: Session
) -> list[Movie]:
    query = select(MoviesOrm)
    result = [Movie.model_validate(row, from_attributes=True) for row in db.execute(query).all()]

    return result


def get_genres_to_movie(
        movie_id: int,
        db: Session
) -> Genre:
    query = (
        select(GenresOrm)
        .join(MovieGenresOrm, GenresOrm.id == MovieGenresOrm.genre_id)
        .join(MoviesOrm, MoviesOrm.id == MovieGenresOrm.movie_id)
        .filter(MoviesOrm.id == movie_id)
    )

    result = Genre.model_validate(db.execute(query).all())

    return result


def get_all_orders(
        db: Session
) -> list[Order]:
    query = select(OrdersOrm)
    result = [Order.model_validate(row, from_attributes=True) for row in db.execute(query).all()]

    return result


def change_seat_status(
        id: int,
        db: Session
):
    query = (
        update(SeatsOrm)
        .where(SeatsOrm.id == id)
        .values(is_available=False)
    )
    db.execute(query)
    db.commit()


def add_order(
        order: OrderCreate,
        db: Session
) -> Order:
    new_order = OrdersOrm(
        user_id=order.user_id,
        session_id=order.session_id,
        total_price=order.total_price,
        info=order.info
    )

    for seat_id in order.seats_ids:
        change_seat_status(seat_id, db)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return Order.model_validate(new_order)

def get_movie_by_id(
        id: int,
        db: Session
) -> Movie:
    query = select(MoviesOrm).where(MoviesOrm.id == id)
    movie = db.execute(query).first()
    result = Movie.model_validate(movie, from_attributes=True)

    return result


def get_hall_by_id(
        id: int,
        db: Session
) -> Hall:
    query = select(HallsOrm).where(HallsOrm.id == id)
    hall = db.execute(query).first()
    result = Hall.model_validate(hall, from_attributes=True)

    return result


def get_session_by_id(
        id: int,
        db: Session
) -> SessionSchema:
    query = select(SessionsOrm).where(SessionsOrm.id == id)
    session = db.execute(query).scalars().first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    result = SessionSchema.model_validate(session, from_attributes=True)

    return result


def get_detailed_session(
        id: int,
        db: Session
) -> SessionDetailed:
    session = get_session_by_id(id, db)
    movie = get_movie_by_id(session.movie_id, db)
    hall = get_hall_by_id(session.hall_id, db)

    session_detailed = SessionDetailed(
        id=session.id,
        movie=movie,
        hall=hall,
        start_time=session.start_time
    )

    return session_detailed


def get_seats_for_order(
        order_id: int,
        db: Session
) -> list[Seat]:
    query = (
        select(SeatsOrm)
        .join(SessionsOrm, SeatsOrm.hall_id == SessionsOrm.hall_id)
        .join(OrdersOrm, SessionsOrm.id == OrdersOrm.session_id)
        .where(OrdersOrm.id == order_id)
    )

    result = [Seat.model_validate(row, from_attributes=True) for row in db.execute(query).all()]

    return result


def get_user_by_id(
        id: int,
        db: Session
) -> User:
    query = select(UsersOrm).where(UsersOrm.id == id)
    user = db.execute(query).first()
    result = User.model_validate(user, from_attributes=True)

    return result

def get_user_by_email(
        email: str,
        db: Session
) -> User:
    query = select(UsersOrm).where(UsersOrm.email == email)
    user = db.execute(query).scalars().first()
    print(user)
    result = User.model_validate(user, from_attributes=True)

    return result


def get_user_orders(
        user_id: int,
        db: Session
) -> list[OrderDetailed]:
    query = select(OrdersOrm).where(OrdersOrm.user_id == user_id)
    orders = [
        Order.model_validate(row, from_attributes=True)
        for row in db.execute(query).scalars().all()
    ]

    result = [
        OrderDetailed(
            **order.model_dump(),
            seats=get_seats_for_order(order.id, db)
        ) for order in orders
    ]

    return result


def get_all_users_orders(
        db: Session
) -> list[UserWithOrders]:
    users = [
        User.model_validate(row, from_attributes=True)
        for row in db.execute(select(UsersOrm)).scalars().all()
    ]
    result = [
        UserWithOrders(
            user=user,
            orders=get_user_orders(user.id, db)
        )
        for user in users
    ]

    return result

def get_seats_for_session(
        session_id: int,
        db: Session
) -> list[Seat]:
    query = (
        select(SeatsOrm)
        .join(SessionsOrm, SeatsOrm.hall_id == SessionsOrm.hall_id)
        .where(SessionsOrm.id == session_id)
    )

    result = [Seat.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result

def get_sessions(
        db: Session
) -> list[SessionSchema]:
    sessions = [
        SessionSchema.model_validate(row, from_attributes=True)
        for row in db.execute(select(SessionsOrm)).scalars().all()
    ]

    return sessions