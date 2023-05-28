from fastapi import FastAPI
import ffp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from Fowzy"}

@app.get("/get_pics/id={id}&lastName={lastName}")

def get_pics(id: int, lastName: str):
    path = ffp.run(id, lastName)
    return {"id": id, "lastName": lastName, "path": path}