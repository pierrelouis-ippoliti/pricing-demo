from app.models import Customer, Order, OrderItem
from app.pricing import calculate_price

customer = Customer(id="c1", name="Hugo")
order = Order(id="o1", customer=customer, coupon_code="WELCOME10")
order.items = [OrderItem(product_id="p1", name="Widget", unit_price=20.0, quantity=5)]

result = calculate_price(order)
print(result)