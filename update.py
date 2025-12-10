import time
from schemas.schemas_orders import the_redis, Order

key = 'refund-order'
group = 'payment'

try:
    the_redis.xgroup_create(name=key, groupname=group, mkstream=True)
except Exception as e:
    print(str(e))

while True:
    try:
        results = the_redis.xreadgroup(groupname=group, consumername=key, streams={key: '>'})
        print(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]

                order = Order.get(obj["pk"])
                order.status = "refunded"
                order.save()
    except Exception as e:
        print(str(e))
    time.sleep(3)