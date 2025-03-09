from fastapi import FastAPI,Query
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Hotel A", "price": 100},
    {"id": 2, "title": "Hotel B", "price": 200},
    {"id": 3, "title": "Hotel C", "price": 300},
]


@app.get("/hotels")
def get_hotels(
        title: str | None = Query(None, description="Hotel title"),
):
    return [hotel for hotel in hotels if hotel ["title"] == title]




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8002)