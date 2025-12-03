from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from dotenv import load_dotenv
import os

app = FastAPI()

origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Access-Control-Allow-Origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

redis_password = os.environ.get("REDIS_PASSWORD")

if redis_password is None:
    raise Exception("No redis password found.")

redis = get_redis_connection(
    host="redis-11913.c321.us-east-1-2.ec2.cloud.redislabs.com",
    port=11913,
    password=redis_password,
    decode_responses=True,
)