import pytest

from app.discounts import apply_discounts, coupon_discount, volume_discount
from app.models import Customer, Order, OrderItem
from app.pricing import calculate_price


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def standard_customer():
    return Customer(id="c1", name="Alice", is_premium=False)


@pytest.fixture
def premium_customer():
    return Customer(id="c2", name="Bob", is_premium=True)


def make_order(customer, quantities_and_prices, coupon_code=None):
    items = [
        OrderItem(product_id=f"p{i}", name=f"Product {i}", unit_price=price, quantity=qty)
        for i, (qty, price) in enumerate(quantities_and_prices, start=1)
    ]
    return Order(id="o1", customer=customer, items=items, coupon_code=coupon_code)


# ---------------------------------------------------------------------------
# Unit tests — discount components
# ---------------------------------------------------------------------------


def test_volume_discount_below_threshold():
    assert volume_discount(3) == 0.0


def test_volume_discount_at_small_threshold():
    assert volume_discount(5) == 0.10


def test_volume_discount_above_small_threshold():
    assert volume_discount(7) == 0.10


def test_volume_discount_at_large_threshold():
    assert volume_discount(10) == 0.15


def test_volume_discount_above_large_threshold():
    assert volume_discount(25) == 0.15


def test_coupon_discount_known_code():
    assert coupon_discount("WELCOME10") == 0.10
    assert coupon_discount("SUMMER20") == 0.20
    assert coupon_discount("VIP15") == 0.15


def test_coupon_discount_unknown_code():
    assert coupon_discount("FAKE99") == 0.0


def test_coupon_discount_none():
    assert coupon_discount(None) == 0.0


# ---------------------------------------------------------------------------
# Integration tests — calculate_price
# ---------------------------------------------------------------------------


def test_no_discount(standard_customer):
    order = make_order(standard_customer, [(2, 50.0)])
    result = calculate_price(order)

    assert result["subtotal"] == 100.0
    assert result["discount_rate"] == 0.0
    assert result["discount_amount"] == 0.0
    assert result["tax"] == 20.0
    assert result["total"] == 120.0


def test_volume_discount_applied(standard_customer):
    # 5 items × €20 = €100 subtotal, 10% volume discount
    order = make_order(standard_customer, [(5, 20.0)])
    result = calculate_price(order)

    assert result["subtotal"] == 100.0
    assert result["discount_rate"] == 0.10
    assert result["discount_amount"] == 10.0
    assert result["tax"] == pytest.approx(18.0)
    assert result["total"] == pytest.approx(108.0)


def test_coupon_discount_applied(standard_customer):
    order = make_order(standard_customer, [(2, 50.0)], coupon_code="WELCOME10")
    result = calculate_price(order)

    assert result["discount_rate"] == 0.10
    assert result["discount_amount"] == 10.0
    assert result["total"] == pytest.approx(108.0)


def test_volume_and_coupon_combined(standard_customer):
    # 5 items = 10% volume + WELCOME10 = 10% coupon → 20% total
    order = make_order(standard_customer, [(5, 20.0)], coupon_code="WELCOME10")
    result = calculate_price(order)

    assert result["discount_rate"] == 0.20
    assert result["discount_amount"] == 20.0
    assert result["total"] == pytest.approx(96.0)


def test_discount_cap_applied(standard_customer):
    # 10 items = 15% volume + SUMMER20 = 20% coupon → 35% raw, capped at 25%
    order = make_order(standard_customer, [(10, 10.0)], coupon_code="SUMMER20")
    result = calculate_price(order)

    assert result["discount_rate"] == 0.25
    assert result["discount_amount"] == 25.0
    assert result["total"] == pytest.approx(90.0)


def test_tax_is_applied_after_discount(standard_customer):
    # €200 subtotal, no discount → tax on full amount
    order = make_order(standard_customer, [(2, 100.0)])
    result = calculate_price(order)

    assert result["tax"] == 40.0
    assert result["total"] == 240.0


def test_empty_order(standard_customer):
    order = make_order(standard_customer, [])
    result = calculate_price(order)

    assert result["subtotal"] == 0.0
    assert result["total"] == 0.0


def test_unknown_coupon_gives_no_discount(standard_customer):
    order = make_order(standard_customer, [(2, 50.0)], coupon_code="INVALID")
    result = calculate_price(order)

    assert result["discount_rate"] == 0.0
    assert result["total"] == 120.0
