from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Hotel A", "price": 100},
    {"id": 2, "title": "Hotel B", "price": 200},
    {"id": 3, "title": "Hotel C", "price": 300},
]

@app.get("/hotels")
def get_hotels(
        title: str,
):
    return [hotel for hotel in hotels if hotel["title"] == title]


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotel = {"id": len(hotels) + 1, "title": title}
    hotels.append(hotel)
    return hotel
@app.put("/hotels{id}")
def update_hotel(
        id: int,
        title: str = Body(embed=True),
):
    hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
    if hotel:
        hotel["title"] = title
        return hotel
    return {"message": "Hotel not found"}
@app.patch("/hotels{id}")
def patch_hotel(
        id: int,
        title: str = Body(embed=True),
):
    hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
    if hotel:
        hotel["title"] = title
        return hotel
    return {"message": "Hotel not found"}

@app.delete("/hotels{id}")
def delete_hotel(id: int):
    hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
    if hotel:
        hotels.remove(hotel)
        return {"message": "Hotel deleted successfully"}
    return {"message": "Hotel not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8002)