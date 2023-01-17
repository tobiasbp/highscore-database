from fastapi import FastAPI, HTTPException, Request
import uvicorn
from deta import Deta
import os

app = FastAPI()

# To run the program on your own machine, you must have the deta project key stored in "DETA_PROJECT_KEY"
# To set the environment, use the command "export DETA_PROJECT_KEY={ a deta project key }"
# If the program is run in a micro, the environment variable is already configued to the project key.
deta = Deta()

game_list = deta.Base("games")
score_list = deta.Base("scores")

# Example data which will come from a database in the future
#game_list = [
#    {
#    	"id": 0,
#        "name": "Space Invaders"
#    }, 
#    {
#        "id": 1,
#        "name": "Pac-Man"
#    },
#    {
#        "id": 2,
#        "name": "Donkey Kong"
#    }
#]

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
    """
    Get the first ten games
    """
    fetch_res = game_list.fetch({}, limit=10)
    return {"games": [{"id": game["id"], "name": game["name"]} for game in fetch_res.items], "last": fetch_res.last}

@app.get("/v1/games/{id}")
async def games(id):
    """
    Get a single game by id
    """
    fetch_res = game_list.fetch({"id": int(id)}, limit=1)
    print(fetch_res.items)
    return {"id": fetch_res.items[0]["id"], "name": fetch_res.items[0]["name"]}

@app.post("/v1/games/")
async def games(request: Request):
    game_data = await request.json()
    id = len(game_list)
    game_list.insert({
    	"id": id,
    	"name": game_data["name"]
    })
    return game_list[id]

"""
if type(id) == type(int()):
     for i, game in enumerate(game_list):
         if str(game["id"]) == id:
             return {"id": game["id"], "name": game["name"], "scores": score_list[i]["scores"]}
"""

# This is code
@app.get("/v1/scores/{id}")
async def scores(id):
    """
    
    """
    game_res = game_list.fetch({"id": id}, limit=1)
    if len(game_res.items) != 0:
        score_res = score_list.fetch({"id": id}, limit=10)
        return {"id": game_res.items[0]["id"], "name": game_res.items[0]["name"], "scores": [{"score": s["score"], "user": s["user"]} for s in score_res.items]}
    else:
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
