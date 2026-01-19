import reflex as rx
from typing import Optional
from app.states.models import PurchaseOrder, LineItem, Product
from app.states.auth_state import AuthState
from app.states.vendor_state import VendorState
from app.states.product_state import ProductState
import uuid
from datetime import datetime
import logging


class OrderState(rx.State):
    """State for managing Purchase Orders."""

    orders: list[PurchaseOrder] = [
        {
            "id": "PO-2023-001",
            "vendor_id": "v1",
            "created_by_user_id": "u1",
            "date": "2023-10-15 09:30:00",
            "status": "Approved",
            "total_amount": 5459.5,
        },
        {
            "id": "PO-2023-002",
            "vendor_id": "v2",
            "created_by_user_id": "u1",
            "date": "2023-10-16 14:15:00",
            "status": "Pending",
            "total_amount": 1250.0,
        },
        {
            "id": "PO-2023-003",
            "vendor_id": "v3",
            "created_by_user_id": "u1",
            "date": "2023-10-18 10:00:00",
            "status": "Rejected",
            "total_amount": 5000.0,
        },
        {
            "id": "PO-2023-004",
            "vendor_id": "v4",
            "created_by_user_id": "u1",
            "date": "2023-10-20 11:45:00",
            "status": "Approved",
            "total_amount": 8500.25,
        },
        {
            "id": "PO-2023-005",
            "vendor_id": "v1",
            "created_by_user_id": "u1",
            "date": "2023-10-22 16:20:00",
            "status": "Pending",
            "total_amount": 230.0,
        },
    ]
    line_items: list[LineItem] = [
        {
            "id": "li1",
            "po_id": "PO-2023-001",
            "product_id": "p1",
            "quantity": 10,
            "unit_price": 45.99,
            "total_price": 459.9,
        },
        {
            "id": "li2",
            "po_id": "PO-2023-001",
            "product_id": "p2",
            "quantity": 20,
            "unit_price": 120.5,
            "total_price": 2410.0,
        },
        {
            "id": "li3",
            "po_id": "PO-2023-002",
            "product_id": "p3",
            "quantity": 100,
            "unit_price": 8.75,
            "total_price": 875.0,
        },
        {
            "id": "li4",
            "po_id": "PO-2023-002",
            "product_id": "p4",
            "quantity": 25,
            "unit_price": 15.2,
            "total_price": 380.0,
        },
        {
            "id": "li5",
            "po_id": "PO-2023-003",
            "product_id": "p5",
            "quantity": 20,
            "unit_price": 250.0,
            "total_price": 5000.0,
        },
    ]
    page: int = 1
    items_per_page: int = 10
    is_create_modal_open: bool = False
    new_order_vendor_id: str = ""
    is_add_item_modal_open: bool = False
    current_order_id: str = ""
    new_item_product_id: str = ""
    new_item_quantity: int = 1

    @rx.var
    def total_orders(self) -> int:
        return len(self.orders)

    @rx.var
    def total_pages(self) -> int:
        return (self.total_orders + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def paginated_orders(self) -> list[PurchaseOrder]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        sorted_orders = sorted(self.orders, key=lambda x: x["date"], reverse=True)
        return sorted_orders[start:end]

    @rx.var
    def current_order(self) -> PurchaseOrder:
        order_id = self.router.page.params.get("order_id", "")
        found = [o for o in self.orders if o["id"] == order_id]
        if found:
            return found[0]
        return {
            "id": "",
            "vendor_id": "",
            "created_by_user_id": "",
            "date": "",
            "status": "",
            "total_amount": 0.0,
        }

    @rx.var
    def current_order_lines(self) -> list[LineItem]:
        order_id = self.router.page.params.get("order_id", "")
        return [li for li in self.line_items if li["po_id"] == order_id]

    @rx.var
    def available_products_for_order(self) -> list[Product]:
        """Get products for the vendor of the current order (or new order)."""
        if self.current_order["id"]:
            vendor_id = self.current_order["vendor_id"]
        elif self.new_order_vendor_id:
            vendor_id = self.new_order_vendor_id
        else:
            return []
        return []

    @rx.event
    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1

    @rx.event
    def prev_page(self):
        if self.page > 1:
            self.page -= 1

    @rx.event
    def open_create_modal(self):
        self.new_order_vendor_id = ""
        self.is_create_modal_open = True

    @rx.event
    def close_create_modal(self):
        self.is_create_modal_open = False

    @rx.event
    def set_new_order_vendor(self, vendor_id: str):
        self.new_order_vendor_id = vendor_id

    @rx.event
    async def create_order(self):
        if not self.new_order_vendor_id:
            yield rx.toast("Please select a vendor.")
            return
        auth = await self.get_state(AuthState)
        current_user_id = auth.current_user["id"]
        new_id = f"PO-{datetime.now().year}-{str(uuid.uuid4())[:6].upper()}"
        new_order: PurchaseOrder = {
            "id": new_id,
            "vendor_id": self.new_order_vendor_id,
            "created_by_user_id": current_user_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending",
            "total_amount": 0.0,
        }
        self.orders.insert(0, new_order)
        self.is_create_modal_open = False
        yield rx.toast(f"Order {new_id} created successfully.")
        yield rx.redirect(f"/orders/{new_id}")

    @rx.event
    def open_add_item_modal(self):
        self.new_item_product_id = ""
        self.new_item_quantity = 1
        self.is_add_item_modal_open = True

    @rx.event
    def close_add_item_modal(self):
        self.is_add_item_modal_open = False

    @rx.event
    def set_new_item_product(self, product_id: str):
        self.new_item_product_id = product_id

    @rx.event
    def set_new_item_quantity(self, qty: str):
        try:
            self.new_item_quantity = int(qty)
        except ValueError as e:
            logging.exception(f"Error setting new item quantity: {e}")
            self.new_item_quantity = 1

    @rx.event
    async def add_line_item(self):
        if not self.new_item_product_id:
            yield rx.toast("Please select a product.")
            return
        product_state = await self.get_state(ProductState)
        product = next(
            (p for p in product_state.products if p["id"] == self.new_item_product_id),
            None,
        )
        if not product:
            yield rx.toast("Product not found.")
            return
        order_id = self.router.page.params.get("order_id")
        total_price = product["price"] * self.new_item_quantity
        new_item: LineItem = {
            "id": f"li-{str(uuid.uuid4())[:8]}",
            "po_id": order_id,
            "product_id": product["id"],
            "quantity": self.new_item_quantity,
            "unit_price": product["price"],
            "total_price": total_price,
        }
        self.line_items.append(new_item)
        if order_id:
            self._recalculate_order_total(order_id)
        self.is_add_item_modal_open = False
        yield rx.toast("Item added to order.")

    @rx.event
    def remove_line_item(self, item_id: str):
        item = next((i for i in self.line_items if i["id"] == item_id), None)
        if item:
            order_id = self.router.page.params.get("order_id")
            self.line_items = [i for i in self.line_items if i["id"] != item_id]
            if order_id:
                self._recalculate_order_total(order_id)
            yield rx.toast("Item removed.")

    def _recalculate_order_total(self, order_id: str):
        total = sum(
            (
                item["total_price"]
                for item in self.line_items
                if item["po_id"] == order_id
            )
        )
        for i, o in enumerate(self.orders):
            if o["id"] == order_id:
                self.orders[i]["total_amount"] = total
                break

    @rx.event
    def update_status(self, status: str):
        order_id = self.router.page.params.get("order_id")
        for i, o in enumerate(self.orders):
            if o["id"] == order_id:
                self.orders[i]["status"] = status
                break
        yield rx.toast(f"Order status updated to {status}.")