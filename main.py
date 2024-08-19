from fastapi import FastAPI
from MovieRecSysModel import hybrid_recommendations, get_all_movies


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/recommendations/{title}/{year}/{user_id}")
def read_item(title: str, year: int, user_id: int):
    #capitalize the first letter of each word in the title
    title = title.title()
    title = title + " (" + str(year) + ")"
    recommendations = hybrid_recommendations(user_id, title, 10)
    return {"recommendations": recommendations.to_list()}

@app.get("/movies")
def read_movies():
    movies = get_all_movies()
    return {"movies": movies }