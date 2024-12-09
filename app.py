from fastapi import FastAPI
from fastapi.responses import FileResponse

from parser import main

app = FastAPI()

main()

@app.get("/")
async def root():
    return FileResponse("response.json")