from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Customer:
    id: str
    name: str
    is_premium: bool = False

    def __repr__(self) -> str:
        tier = "premium" if self.is_premium else "standard"
        return f"Customer({self.name!r}, {tier})"


@dataclass
class OrderItem:
    product_id: str
    name: str
    unit_price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity


@dataclass
class Order:
    id: str
    customer: Customer
    items: list[OrderItem] = field(default_factory=list)
    coupon_code: Optional[str] = None

    @property
    def subtotal(self) -> float:
        return sum(item.subtotal for item in self.items)

    @property
    def total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)
