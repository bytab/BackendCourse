from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine #debug
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
async def get_hotels(
         pagination: PaginationDep,
         location: str | None = Query(None, description="Локация отеля(Город или улица)"),
         title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if location:
            query=query.where(HotelsORM.location.ilike(f"%{location}%"))
        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        #print (type(hotels),hotels)
        return hotels

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "New York",
        "value": {
            "title": "New York Skyline Apartment",
            "location": "New York, 5th Avenue"
        }
    },
    "2": {
        "summary": "London",
        "value": {
            "title": "London River View",
            "location": "London, Baker Street"
        }
    },
    "3": {
        "summary": "Paris",
        "value": {
            "title": "Paris Eiffel Retreat",
            "location": "Paris, Champs-Élysées"
        }
    },
    "4": {
        "summary": "Tokyo",
        "value": {
            "title": "Tokyo Central Apartment",
            "location": "Tokyo, Shibuya"
        }
    },
    "5": {
        "summary": "Sydney",
        "value": {
            "title": "Sydney Harbour Residence",
            "location": "Sydney, George Street"
        }
    },
    "6": {
        "summary": "Berlin",
        "value": {
            "title": "Berlin Historic Loft",
            "location": "Berlin, Friedrichstraße"
        }
    },
    "7": {
        "summary": "Toronto",
        "value": {
            "title": "Toronto Downtown Suite",
            "location": "Toronto, Yonge Street"
        }
    },
    "8": {
        "summary": "Moscow",
        "value": {
            "title": "Moscow Kremlin View",
            "location": "Moscow, Tverskaya Street"
        }
    },
    "9": {
        "summary": "Dubai",
        "value": {
            "title": "Dubai Marina Luxury",
            "location": "Dubai, Sheikh Zayed Road"
        }
    },
    "10": {
        "summary": "Rome",
        "value": {
            "title": "Rome Colosseum View",
            "location": "Rome, Via del Corso"
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) #debug
        await session.execute(add_hotel_stmt)
        await session.commit()



    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}