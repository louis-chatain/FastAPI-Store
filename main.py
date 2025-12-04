import time
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
import requests
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


class ProductOrder(HashModel):
    product_id: str
    quantity: int

    class Meta:
        database = redis


class Order(HashModel):
    product_id: str
    name: str
    price: float
    quantity: int
    fee: float
    total: float
    status: str

    class Meta:
        database = redis



@app.post("/orders")
def create(productOrder: ProductOrder, bg_tasks: BackgroundTasks):
    req = requests.get(f"http://localhost:8000/product/{productOrder.product_id}")
    product = req.json()
    the_fee = product["price"] * 0.2
    order = Order(
        product_id = productOrder.product_id,
        name = product["name"],
        price = product["price"],
        quantity = productOrder.quantity,
        fee = the_fee,
        total = (productOrder.quantity * product["price"]) * 0.2,
        status = "pending",
    )
    order.save()

    bg_tasks.add_task(order_complete, order)

    return order


def format(pk: str):
  order = Order.get(pk)
  return {
    'id': order.pk,
    'product_id': order.product_id,
    'product_name': order.name,
    'fee': order.fee,
    'total': order.total,
    'quantity': order.quantity,
    'status': order.status
  }


@app.get("/orders/read_all_pk")
def read_all():
    order = Order.all_pks()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order pk not found. database empty boy.")
    return [format(pk) for pk in order]


@app.get("/orders/{pk}")
def read(pk: str):
    order = Order.get(pk)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order pk {pk} not found.")
    return order


@app.delete("/order/delete")
def delete(pk: str):
    order = Order.delete(pk)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order pk {pk} not found.")
    return order


def order_complete(order: Order):
    time.sleep(10)
    order.status = "Complete"
    order.save()