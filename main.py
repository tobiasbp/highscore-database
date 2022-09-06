from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Example data which will come from a database in the future
games = [
    {
    	"id": 0,
        "name": "Space Invaders",
    }, 
    {
        "id": 1,
        "name": "Pac-Man"
    },
    {
        "id": 2,
        "name": "Donkey Kong"
    }
]

@app.get("/")
def index():
    return {"message": "Hello, world!"}

@app.get("/v1/games/")
def index():
    return games

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=6050, reload=True)
