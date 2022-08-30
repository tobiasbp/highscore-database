from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=6050, reload=True)
