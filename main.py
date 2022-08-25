from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="192.168.0.180", port=6020, reload=True)