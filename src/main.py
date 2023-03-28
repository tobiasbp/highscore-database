from typing import Union, TypedDict

from fastapi import FastAPI, HTTPException, Request
from deta import Deta
#import uvicorn

class Query(TypedDict):
    name: str
    klov_id: int
    key: str

# When running on a Micro, no project
# key is needed here as it's on the micro.
app = FastAPI()


deta = Deta()


games = deta.Base("games")

# A few sample games
game_data = [
    {"name": "Space Invaders", "klov-id": "9662", "key": "g2y9a6nl0lbb"},
    {"name": "Donkey Kong", "klov-id": "7610", "key": "w83if6lv023r"}
    ]

# Add games to database
for game in game_data:
    r = games.put(data=game)
    print(f"Added game to database: {r}")


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

# FIXME: Query is a dict, not a str
@app.get("/v1/games/")
async def get_games(
    query: Union[str, None] = None,
    limit: int = 100,
    last: Union[str, None] = None):
    """
    Get a paginated list of all games
    """
    return games.fetch(query=query, limit=limit, last=last)

@app.get("/v1/games/{key}")
async def get_game(key: str):
    """
    Get a single game
    """
    return games.get(key)

"""
@app.get("/v1/scores/{id}")
async def scores(id):

    return games.get(id, {"error": f"Unknown game ID: {id}"}) 

    #raise HTTPException(status_code=404, detail=f"Game with id '{id}' not found")

@app.post("/v1/games/")
async def games(request: Request):
    game_data = await request.json()
    print(game_data)
    print(game_data["name"])
    id = len(game_list)
    game_list.append({"id": id, "name": game_data["name"]})
    return game_list[id]


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
"""

#if __name__ == '__main__':
#    uvicorn.run("main:app", host="localhost", port=6050, reload=True)
