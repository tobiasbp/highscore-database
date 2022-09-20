from fastapi import FastAPI, HTTPException, Request
import uvicorn

app = FastAPI()

# Example data which will come from a database in the future
game_list = [
    {
    	"id": 0,
        "name": "Space Invaders"
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

score_list = [
    {
    	"id": 0,
        "scores": [
            {"score": 1000, "user": "Xx_Epic_Gamer_xX"},
            {"score": 500, "user": "MemeWizard42"},
            {"score": 200, "user": "Noob1234"}
        ]
    }, 
    {
        "id": 1,
        "scores": [
            {"score": 1000, "user": "Xx_Epic_Gamer_xX"},
            {"score": 500, "user": "MemeWizard42"},
            {"score": 200, "user": "Noob1234"}
        ]
    },
    {
        "id": 2,
        "scores": [
            {"score": 1000, "user": "Xx_Epic_Gamer_xX"},
            {"score": 500, "user": "MemeWizard42"},
            {"score": 200, "user": "Noob1234"}
        ]
    }
]

@app.get("/")
async def index():
    return {"message": "Hello, world!"}

@app.get("/v1/games/")
async def games():
    return [{"id": game["id"], "name": game["name"]} for game in game_list]

@app.get("/v1/scores/{id}")
async def scores(id):
    for i, game in enumerate(game_list):
        if str(game["id"]) == id:
            return {"id": game["id"], "name": game["name"], "scores": score_list[i]["scores"]}
    raise HTTPException(status_code=404, detail=f"Game with id '{id}' not found")

@app.post("/v1/scores/{id}")
async def scores(id, request: Request):
    for i, game in enumerate(game_list):
        if str(game["id"]) == id:
            print(await request.json()) 
            pass
    raise HTTPException(status_code=404, detail=f"Game with id '{id}' not found")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=6050, reload=True)
