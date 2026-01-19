import reflex as rx
from typing import Optional
from app.states.models import Vendor, Product
import random
import logging


class VendorState(rx.State):
    """State for managing Vendors and their associated products."""

    vendors: list[Vendor] = [
        {
            "id": "v1",
            "name": "Acme Industrial Supply",
            "contact_name": "John Smith",
            "phone": "(555) 123-4567",
            "email": "john.smith@acme.com",
            "orders_email": "orders@acme.com",
            "address": "123 Industrial Way, Tech City, CA 90210",
            "credit_limit": 50000.0,
            "total_orders": 145,
        },
        {
            "id": "v2",
            "name": "Global Tech Components",
            "contact_name": "Sarah Connor",
            "phone": "(555) 987-6543",
            "email": "sarah@globaltech.com",
            "orders_email": "sales@globaltech.com",
            "address": "456 Silicon Ave, San Jose, CA 95134",
            "credit_limit": 75000.0,
            "total_orders": 89,
        },
        {
            "id": "v3",
            "name": "FastTrack Logistics",
            "contact_name": "Mike Ross",
            "phone": "(555) 456-7890",
            "email": "mike@fasttrack.com",
            "orders_email": "dispatch@fasttrack.com",
            "address": "789 Logistics Blvd, Dallas, TX 75201",
            "credit_limit": 25000.0,
            "total_orders": 210,
        },
        {
            "id": "v4",
            "name": "Precision Parts Inc.",
            "contact_name": "Emily Blunt",
            "phone": "(555) 222-3333",
            "email": "emily@precision.com",
            "orders_email": "orders@precision.com",
            "address": "321 Machining Ln, Detroit, MI 48201",
            "credit_limit": 100000.0,
            "total_orders": 56,
        },
    ]
    search_query: str = ""
    is_modal_open: bool = False
    editing_vendor_id: str = ""
    form_name: str = ""
    form_contact: str = ""
    form_phone: str = ""
    form_email: str = ""
    form_orders_email: str = ""
    form_address: str = ""
    form_credit: float = 0.0

    @rx.var
    def filtered_vendors(self) -> list[Vendor]:
        if not self.search_query:
            return self.vendors
        query = self.search_query.lower()
        return [
            v
            for v in self.vendors
            if query in v["name"].lower()
            or query in v["contact_name"].lower()
            or query in v["email"].lower()
        ]

    @rx.var
    def active_vendor(self) -> Vendor:
        """Get the vendor details based on the URL parameter."""
        vendor_id = self.router.page.params.get("vendor_id", "")
        found = [v for v in self.vendors if v["id"] == vendor_id]
        if found:
            return found[0]
        return {
            "id": "",
            "name": "Vendor Not Found",
            "contact_name": "-",
            "phone": "-",
            "email": "-",
            "orders_email": "-",
            "address": "-",
            "credit_limit": 0.0,
            "total_orders": 0,
        }

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def open_add_modal(self):
        self.editing_vendor_id = ""
        self.form_name = ""
        self.form_contact = ""
        self.form_phone = ""
        self.form_email = ""
        self.form_orders_email = ""
        self.form_address = ""
        self.form_credit = 0.0
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, vendor: Vendor):
        self.editing_vendor_id = vendor["id"]
        self.form_name = vendor["name"]
        self.form_contact = vendor["contact_name"]
        self.form_phone = vendor["phone"]
        self.form_email = vendor["email"]
        self.form_orders_email = vendor["orders_email"]
        self.form_address = vendor["address"]
        self.form_credit = vendor["credit_limit"]
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def update_form_field(self, field: str, value: str):
        if field == "name":
            self.form_name = value
        elif field == "contact":
            self.form_contact = value
        elif field == "phone":
            self.form_phone = value
        elif field == "email":
            self.form_email = value
        elif field == "orders_email":
            self.form_orders_email = value
        elif field == "address":
            self.form_address = value

    @rx.event
    def update_credit_field(self, value: str):
        try:
            self.form_credit = float(value)
        except ValueError as e:
            logging.exception(f"Error converting credit field: {e}")

    @rx.event
    def save_vendor(self):
        if self.editing_vendor_id:
            for i, v in enumerate(self.vendors):
                if v["id"] == self.editing_vendor_id:
                    self.vendors[i] = {
                        "id": self.editing_vendor_id,
                        "name": self.form_name,
                        "contact_name": self.form_contact,
                        "phone": self.form_phone,
                        "email": self.form_email,
                        "orders_email": self.form_orders_email,
                        "address": self.form_address,
                        "credit_limit": self.form_credit,
                        "total_orders": v["total_orders"],
                    }
                    break
            yield rx.toast("Vendor updated successfully.")
        else:
            import uuid

            new_id = f"v-{str(uuid.uuid4())[:8]}"
            new_vendor: Vendor = {
                "id": new_id,
                "name": self.form_name,
                "contact_name": self.form_contact,
                "phone": self.form_phone,
                "email": self.form_email,
                "orders_email": self.form_orders_email,
                "address": self.form_address,
                "credit_limit": self.form_credit,
                "total_orders": 0,
            }
            self.vendors.append(new_vendor)
            yield rx.toast("New vendor added successfully.")
        self.is_modal_open = False

    @rx.event
    async def delete_vendor(self, vendor_id: str):
        self.vendors = [v for v in self.vendors if v["id"] != vendor_id]
        from app.states.product_state import ProductState

        product_state = await self.get_state(ProductState)
        product_state.products = [
            p for p in product_state.products if p["vendor_id"] != vendor_id
        ]
        yield rx.toast("Vendor deleted successfully.")
        current_param_id = self.router.page.params.get("vendor_id")
        if current_param_id == vendor_id:
            yield rx.redirect("/vendors")

    @rx.event
    def navigate_to_vendor(self, vendor_id: str):
        return rx.redirect(f"/vendors/{vendor_id}")