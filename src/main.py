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
players = deta.Base("players")
scores = deta.Base("scores")

# Users have access to the database and can modify data
# Players are accounts connected to scores

# Contains a unique token
# Token allows you to manipulate the database
access_tokens = deta.Base("access_tokens")

# A few sample games
game_data = [
    {"name": "Space Invaders", "klov-id": "9662", "key": "g2y9a6nl0lbb"},
    {"name": "Donkey Kong", "klov-id": "7610", "key": "w83if6lv023r"}
]

# Add games to database
for game in game_data:
    r = games.put(data=game)
    print(f"Added game to database: {r}")

player_data = [
    {"name": "Xx_Epic_Gamer_xX", "key": "sffa5zwu38di"},
    {"name": "MemeWizard42", "key": "fbd1opqszmht"},
    {"name": "Noob1234", "key": "dj3usnatdbi4"}
]

# Add players to database
for p in player_data:
    players.put(data=p)

score_data = [
    {"game_key": "g2y9a6nl0lbb", "score": 1000, "player_key": "sffa5zwu38di", "key": "td38yf6k4n5y"},
    {"game_key": "g2y9a6nl0lbb", "score": 1100, "player_key": "fbd1opqszmht", "key": "2ouqv1h0g3t3"},
    {"game_key": "w83if6lv023r", "score": 5800, "player_key": "fbd1opqszmht", "key": "qbom1524u1r7"},
    {"game_key": "w83if6lv023r", "score": 9800, "player_key": "dj3usnatdbi4", "key": "90mx0waulyxq"},
    {"game_key": "w83if6lv023r", "score": 6600, "player_key": "sffa5zwu38di", "key": "kelpz1f588z3"},
]

for s in score_data:
    scores.put(s)

# Used to instanciate an access token
# Deta generated key is used as token
#access_tokens.put(data={})


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


@app.get("/v1/games/{game_key}")
async def get_game(game_key: str):
    """
    Get a single game
    """
    return games.get(game_key)


@app.get("/v1/games/{game_key}/scores")
async def get_game_scores(
	game_key: str, 
	limit: int = 100, 
	last: Union[str, None] = None):
    """
    Get scores for a game
    """

    return scores.fetch(query={"game_key": game_key}, limit=limit, last=last)


@app.post("/v1/games/{game_key}/scores")
async def post_game_scores(
	game_key: str,
	player_key: str,
	score: int,
	access_token: str):
	"""
	Post scores on a game
	"""
	
	# Returns the new score item
	# Tests if item with key 'access_token' in access_tokens
	if access_tokens.get(key=access_token):
		return scores.put(data={"game_key": game_key, "score": score, "player_key": player_key})
	else:
		raise HTTPException(status_code=401, detail=f"Invalid access token")


# FIXME: Query is a dict, not a str
@app.get("/v1/players/")
async def get_players(
    query: Union[str, None] = None,
    limit: int = 100,
    last: Union[str, None] = None):
    """
    Get a paginated list of all players
    """
    return players.fetch(query=query, limit=limit, last=last)


@app.post("/v1/players/")
async def post_players(
    name: str,
    access_token: str):
    """
    Create a new player acccount
    """

    # Tests if item with key 'access_token' in access_tokens
    if access_tokens.get(key=access_token):
    	return players.put(data={"name": name})
    else:
        raise HTTPException(status_code=401, detail=f"Invalid access token")


@app.get("/v1/players/{player_key}")
async def get_player(player_key: str):
    """
    Get a single player
    """
    return players.get(player_key)

@app.get("/v1/players/{player_key}/scores")
async def get_player_scores(
	player_key: str,
	limit: int = 100, 
	last: Union[str, None] = None):
	"""
	Get scores for a player
	"""
	return scores.fetch(query={"player_key": player_key}, limit=limit, last=last)
