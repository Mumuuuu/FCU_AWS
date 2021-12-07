#!/usr/bin/python3

from fastapi import FastAPI
import jwt
from hashlib import sha256
from json import loads
from time import time 
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

# Init Database connection and await
class DBinit():
    def __init__(self , url:str):
        self.connect = AsyncIOMotorClient(url)
        self.database = self.connect["FCU_AWS"]
        asyncio.run_coroutine_threadsafe(self.init_connect() , asyncio.get_event_loop())

    async def init_connect(self):
        collections = await self.database.list_collections.names()
        for collect in ["users"]:
            if collect not in colletions:
                await self.database.create_collection(collect)

    async def check_user(self , username:str , password:str) -> dict:
        return await self.database.find_one({
            "username" : username,
            "password" : sha256(password.encode()).hexdigest()
            })

db = DBinit("mongodb://mumu:mumu123123123@114.33.1.57:27000")

@app.get("/login" , method=["POST"])
def login(username:str , password:str):
    db = loads(open("db.json" , "rb").read())
    data = request.json #TODO change into fastapi
    username = data["username"]
    password = sha256(data["password"]).hexdigest()

    res = db.check_user(username , password)
    if(not res):
        return False

    loginTime = int(time.time())
    expiredTime = logintime + 10 * 60 # add 10 minutes 
    payload = ({
            "loginTime" : loginTime ,
            "expiredTime" : expiredTime ,
            "username" : username
            })
    
    return jwt.encode(payload , key="FCU_AWS" , algorithm="HS256")

@app.get("/register" , method=["POST"])
def register():
    pass

