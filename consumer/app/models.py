from enum import Enum, EnumMeta
from pydantic import BaseModel


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class OrdersEvents(str, Enum, metaclass=MetaEnum):
    ORDER_CREATED = "order_created"
    ORDER_CHANGED = "order_changed"
    ORDER_DELETED = "order_deleted"


class OrderData(BaseModel):
    id: int
    id_str: str
    order_type: int
    datetime: str
    microtimestamp: str
    amount: float
    amount_str: str
    amount_traded: str
    amount_at_create: str
    price: int
    price_str: str


class Order(BaseModel):
    data: OrderData
    channel: str
    event: str

    def get_price(self):
        return self.data.price

    def __lt__(self, other):
        return self.data.price < other.data.price

    def __le__(self, other):
        return self.data.price <= other.data.price

    def __eq__(self, other):
        return self.data.price == other.data.price

    def __ne__(self, other):
        return self.data.price != other.data.price

    def __gt__(self, other):
        return self.data.price > other.data.price

    def __ge__(self, other):
        return self.data.price >= other.data.price


class Orders(BaseModel):
    order_created: list[Order] = list()
    order_changed: list[Order] = list()
    order_deleted: list[Order] = list()

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except:
            super().__getitem__(key)

    def __contains__(self, key):
        try:
            return hasattr(self, key)
        except:
            super().__getitem__(key)

    def __setitem__(self, key, value):
        try:
            setattr(self, key, value)
        except:
            super().__getitem__(key)
