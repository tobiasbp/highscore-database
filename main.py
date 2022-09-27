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
    if type(id) == type(int()):
        for i, game in enumerate(game_list):
            if str(game["id"]) == id:
                return {"id": game["id"], "name": game["name"], "scores": score_list[i]["scores"]}
    raise HTTPException(status_code=404, detail=f"Game with id '{id}' not found")

@app.post("/v1/scores/{id}")
async def scores(id, request: Request):
    if id.isdigit():
        for i, game in enumerate(score_list):
            if str(game["id"]) == id:
                score_data = await request.json()
                try:
                    score = int(score_data["score"])
                    user = score_data["user"]
                except ValueError:
                	raise HTTPException(status_code=422, detail=f"Invalid score data: 'score' is not an integer")
                except KeyError:
                	raise HTTPException(status_code=422, detail=f"Invalid score data: missing field")
                game["scores"].append({"score": score, "user": user})
                game["scores"] = sorted(game["scores"], key=lambda d: d["score"])
                game["scores"].reverse()
                rank = 0
                for i, s in enumerate(game["scores"]):
                    if s == {"score": score, "user": user}:
                        rank = i + 1
                return {"rank": rank}
    raise HTTPException(status_code=404, detail=f"Game with id '{id}' not found")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=6050, reload=True)
