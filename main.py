from fastapi import FastAPI
from MovieRecSysModel import hybrid_recommendations, get_all_movies


app = FastAPI()

# allow all origins
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/recommendations/{title}/{user_id}")
def read_item(title: str, user_id: int):
    recommendations = hybrid_recommendations(user_id, title, 10)
    return {"recommendations": recommendations.to_list()}

@app.get("/movies")
def read_movies():
    movies = get_all_movies()
    return {"movies": movies }

# uvicorn main:app --reload --host 0.0.0.0 --port 8000