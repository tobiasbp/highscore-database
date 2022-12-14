# highscore-database

An API allowing for the saving and retrieval of game high scores

You start the api by using the following command
```
python3 main.py
```

You can then test the api by using
```
curl http://localhost:6050/
```

The command should return a valid json response
```
{"message":"Hello, world!"}
```

You can get a list of games and their id
```
curl http://localhost:6050/v1/games/
```

If you want the list of scores on a specific game, you can use the following command replacing the '0' with the id of the game you'd like to retrieve the scores of.
```
curl http://localhost:6050/v1/scores/0
```

# Dependencies

We are building our api with [FastAPI](https://fastapi.tiangolo.com/)

# Setup

### Windows
```
python3 -mvenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Linux
```
python3 -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
