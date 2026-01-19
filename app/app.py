import reflex as rx
from app.pages.vendors import vendors_page
from app.pages.vendor_detail import vendor_detail_page


def index():
    return rx.el.div("Redirecting...", on_mount=rx.redirect("/vendors"))


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.pages.products import products_page
from app.pages.orders import orders_page
from app.pages.order_detail import order_detail_page
from app.pages.reports import reports_page

app.add_page(index, route="/")
app.add_page(vendors_page, route="/vendors")
app.add_page(vendor_detail_page, route="/vendors/[vendor_id]")
app.add_page(products_page, route="/products")
app.add_page(orders_page, route="/orders")
app.add_page(order_detail_page, route="/orders/[order_id]")
app.add_page(reports_page, route="/reports")