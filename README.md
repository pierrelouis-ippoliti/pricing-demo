# pricing-demo

A small Python pricing service used to demonstrate AI coding agent workflows.

## Overview

This service calculates order prices by applying discount rules and tax.

**Discount rules:**

| Rule        | Condition              | Rate |
|-------------|------------------------|------|
| Volume      | 5–9 items              | 10%  |
| Volume      | 10+ items              | 15%  |
| Coupon      | `WELCOME10`            | 10%  |
| Coupon      | `NEOFACTO15`           | 15%  |
| Coupon      | `SUMMER20`             | 20%  |

Discounts are combined and capped at a maximum rate.
Tax (20%) is applied after the discount.

## Setup

```bash
pip install -r requirements.txt
```

## Run tests

```bash
pytest
```

## Project structure

```
pricing-demo/
├── app/
│   ├── models.py       # Customer, Order, OrderItem
│   ├── discounts.py    # Discount rules and cap
│   └── pricing.py      # Price calculation
├── tests/
│   └── test_pricing.py
├── AGENTS.md
└── README.md
```

## Quick example

```python
from app.models import Customer, Order, OrderItem
from app.pricing import calculate_price

customer = Customer(id="c1", name="Alice")
order = Order(id="o1", customer=customer, coupon_code="WELCOME10")
order.items = [OrderItem(product_id="p1", name="Widget", unit_price=20.0, quantity=5)]

result = calculate_price(order)
print(result)
# {'subtotal': 100.0, 'discount_rate': 0.2, 'discount_amount': 20.0, 'tax': 16.0, 'total': 96.0}
```
