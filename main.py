from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from router import order


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

app.include_router(order.router)