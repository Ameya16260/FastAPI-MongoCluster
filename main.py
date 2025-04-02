from fastapi import FastAPI
from model import Password
import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient

from contextlib import asynccontextmanager
username = urllib.parse.quote_plus('Ameya')
password = urllib.parse.quote_plus('Ameya@mongo1234')
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)

async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://%s:%s@cluster0.u936e.mongodb.net/" % (username,password))
    app.mongodb = app.mongodb_client.get_database("Passwords")
    print("MongoDB connected.")

async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")
app = FastAPI(lifespan=lifespan)
@app.get("/allPass",response_model=list[Password])
async def read_root():
    alldata = await app.mongodb["passwords"].find().to_list(length=None)  
    return alldata
@app.post("/savePass",response_model=Password)
async def addPassword(pas:Password):
    result = await app.mongodb["passwords"].insert_one(pas.model_dump())
    savedPass= await app.mongodb["passwords"].find_one({"_id":result.inserted_id})
    return savedPass
    


