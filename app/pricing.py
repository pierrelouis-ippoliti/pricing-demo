from app.discounts import apply_discounts
from app.models import Order

TAX_RATE = 0.20


def calculate_price(order: Order) -> dict:
    """
    Calculate the full price breakdown for an order

    Steps:
      1. Compute subtotal from order items
      2. Apply discounts (volume + coupon, capped)
      3. Apply tax on the discounted amount

    Returns a dict with: subtotal, discount_rate, discount_amount, tax, total
    """
    subtotal = order.subtotal

    if subtotal == 0:
        return {
            "subtotal": 0.0,
            "discount_rate": 0.0,
            "discount_amount": 0.0,
            "tax": 0.0,
            "total": 0.0,
        }

    discount_rate = apply_discounts(order)
    
    discount_amount = subtotal * discount_rate
    after_discount = subtotal - discount_amount
    
    tax = after_discount * TAX_RATE
    total = after_discount + tax

    return {
        "subtotal": round(subtotal, 2),
        "discount_rate": round(discount_rate, 4),
        "discount_amount": round(discount_amount, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
    }
