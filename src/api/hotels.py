from fastapi import APIRouter, Body
from src.repositories.hotels import HotelsRepository
from src.database import async_session_maker
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)

@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()



    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}