from app.models import Order

VALID_COUPONS: dict[str, float] = {
    "WELCOME10": 0.10,
    "SUMMER20": 0.20,
    "NEOFACTO15": 0.15,
}

MAX_DISCOUNT = 0.25  # Maximum allowed discount rate


def volume_discount(total_quantity: int) -> float:
    """
    Return a discount rate based on the total number of items ordered
    """
    
    if total_quantity >= 10:
        return 0.15
    elif total_quantity >= 5:
        return 0.10
    
    return 0.0


def coupon_discount(coupon_code: str | None) -> float:
    """
    Return the discount rate for a given coupon code, or 0.0 if unknown
    """    
    if coupon_code is None:
        return 0.0
    
    return VALID_COUPONS.get(coupon_code, 0.0)


def apply_discounts(order: Order) -> float:
    """
    Compute the final discount rate for an order

    Combines volume and coupon discounts
    The result is capped at MAX_DISCOUNT
    """
    
    discount = volume_discount(order.total_quantity)
    discount += coupon_discount(order.coupon_code)
    
    return min(discount, MAX_DISCOUNT)
