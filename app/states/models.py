import reflex as rx
from typing import TypedDict, Optional


class User(TypedDict):
    id: str
    name: str
    email: str
    role: str
    avatar_url: str


class Vendor(TypedDict):
    id: str
    name: str
    contact_name: str
    phone: str
    email: str
    orders_email: str
    address: str
    credit_limit: float
    total_orders: int


class Product(TypedDict):
    id: str
    vendor_id: str
    part_number: str
    manufacturer: str
    description: str
    price: float
    stock: int


class PurchaseOrder(TypedDict):
    id: str
    vendor_id: str
    created_by_user_id: str
    date: str
    status: str
    total_amount: float


class LineItem(TypedDict):
    id: str
    po_id: str
    product_id: str
    quantity: int
    unit_price: float
    total_price: float