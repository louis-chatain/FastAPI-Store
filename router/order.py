from fastapi import APIRouter
from schemas.schemas_orders import ProductOrder, Order
from fastapi.background import BackgroundTasks
from fastapi import HTTPException, status
import requests
import time


router = APIRouter(prefix="/orders", tags=["orders"])


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


def order_complete(order: Order):
    time.sleep(10)
    order.status = "Complete"
    order.save()


@router.post("/create")
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


@router.get("/read_all_pk")
def read_all():
    order = Order.all_pks()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order pk not found. database empty boy.")
    return [format(pk) for pk in order]


@router.get("/{pk}")
def read(pk: str):
    order = Order.get(pk)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order pk {pk} not found.")
    return order


@router.delete("/delete")
def delete(pk: str):
    order = Order.delete(pk)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order pk {pk} not found.")
    return order
