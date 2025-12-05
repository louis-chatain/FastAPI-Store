from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
import os


load_dotenv() 

redis_password = os.environ.get("REDIS_PASSWORD")

if redis_password is None:
    raise Exception("No redis password found.")

the_redis = get_redis_connection(
    host="redis-11913.c321.us-east-1-2.ec2.cloud.redislabs.com",
    port=11913,
    password=redis_password,
    decode_responses=True,
)


class ProductOrder(HashModel):
    product_id: str
    quantity: int

    class Meta:
        database = the_redis


class Order(HashModel):
    product_id: str
    name: str
    price: float
    quantity: int
    fee: float
    total: float
    status: str

    class Meta:
        database = the_redis