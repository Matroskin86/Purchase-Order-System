import reflex as rx
from typing import Optional
from app.states.models import Product
from app.states.vendor_state import VendorState
import uuid
import logging


class ProductState(rx.State):
    """State for managing Products."""

    products: list[Product] = [
        {
            "id": "p1",
            "vendor_id": "v1",
            "part_number": "ACM-1001",
            "manufacturer": "Acme",
            "description": "Heavy Duty Widget",
            "price": 45.99,
            "stock": 100,
        },
        {
            "id": "p2",
            "vendor_id": "v1",
            "part_number": "ACM-1002",
            "manufacturer": "Acme",
            "description": "Industrial Gear",
            "price": 120.5,
            "stock": 50,
        },
        {
            "id": "p3",
            "vendor_id": "v2",
            "part_number": "GTC-X5",
            "manufacturer": "Global Tech",
            "description": "Microcontroller Unit",
            "price": 8.75,
            "stock": 500,
        },
        {
            "id": "p4",
            "vendor_id": "v2",
            "part_number": "GTC-S2",
            "manufacturer": "Global Tech",
            "description": "Sensor Module",
            "price": 15.2,
            "stock": 200,
        },
        {
            "id": "p5",
            "vendor_id": "v3",
            "part_number": "FTL-BOX",
            "manufacturer": "FastTrack",
            "description": "Shipping Container Standard",
            "price": 250.0,
            "stock": 20,
        },
    ]
    search_query: str = ""
    is_modal_open: bool = False
    editing_product_id: str = ""
    form_part_number: str = ""
    form_manufacturer: str = ""
    form_description: str = ""
    form_price: float = 0.0
    form_vendor_id: str = ""
    form_stock: int = 0

    @rx.var
    def filtered_products(self) -> list[Product]:
        if not self.search_query:
            return self.products
        query = self.search_query.lower()
        return [
            p
            for p in self.products
            if query in p["part_number"].lower()
            or query in p["description"].lower()
            or query in p["manufacturer"].lower()
        ]

    @rx.var
    def vendor_products(self) -> list[Product]:
        """Products for the vendor currently viewed in vendor details page."""
        vendor_id = self.router.page.params.get("vendor_id", "")
        return [p for p in self.products if p["vendor_id"] == vendor_id]

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def open_add_modal(self):
        self.editing_product_id = ""
        self.form_part_number = ""
        self.form_manufacturer = ""
        self.form_description = ""
        self.form_price = 0.0
        self.form_vendor_id = ""
        self.form_stock = 0
        self.is_modal_open = True

    @rx.event
    def open_add_modal_with_vendor(self, vendor_id: str):
        self.editing_product_id = ""
        self.form_part_number = ""
        self.form_manufacturer = ""
        self.form_description = ""
        self.form_price = 0.0
        self.form_vendor_id = vendor_id
        self.form_stock = 0
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, product: Product):
        self.editing_product_id = product["id"]
        self.form_part_number = product["part_number"]
        self.form_manufacturer = product["manufacturer"]
        self.form_description = product["description"]
        self.form_price = product["price"]
        self.form_vendor_id = product["vendor_id"]
        self.form_stock = product["stock"]
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def update_form_field(self, field: str, value: str):
        if field == "part_number":
            self.form_part_number = value
        elif field == "manufacturer":
            self.form_manufacturer = value
        elif field == "description":
            self.form_description = value
        elif field == "vendor_id":
            self.form_vendor_id = value

    @rx.event
    def update_price(self, value: str):
        try:
            self.form_price = float(value)
        except ValueError as e:
            logging.exception(f"Error updating price: {e}")

    @rx.event
    def update_stock(self, value: str):
        try:
            self.form_stock = int(value)
        except ValueError as e:
            logging.exception(f"Error updating stock: {e}")

    @rx.event
    def save_product(self):
        if self.editing_product_id:
            for i, p in enumerate(self.products):
                if p["id"] == self.editing_product_id:
                    self.products[i] = {
                        "id": self.editing_product_id,
                        "vendor_id": self.form_vendor_id,
                        "part_number": self.form_part_number,
                        "manufacturer": self.form_manufacturer,
                        "description": self.form_description,
                        "price": self.form_price,
                        "stock": self.form_stock,
                    }
                    break
            yield rx.toast("Product updated successfully.")
        else:
            new_product: Product = {
                "id": f"p-{str(uuid.uuid4())[:8]}",
                "vendor_id": self.form_vendor_id,
                "part_number": self.form_part_number,
                "manufacturer": self.form_manufacturer,
                "description": self.form_description,
                "price": self.form_price,
                "stock": self.form_stock,
            }
            self.products.append(new_product)
            yield rx.toast("New product added successfully.")
        self.is_modal_open = False

    @rx.event
    def delete_product(self, product_id: str):
        self.products = [p for p in self.products if p["id"] != product_id]
        yield rx.toast("Product deleted.")