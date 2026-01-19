import reflex as rx
from app.components.layout import layout
from app.states.vendor_state import VendorState
from app.states.product_state import ProductState
from app.components.vendor_form import vendor_modal
from app.components.product_form import product_modal


def detail_item(label: str, value: str, icon_name: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.dt(
            rx.cond(
                icon_name != "",
                rx.icon(
                    icon_name, class_name="h-4 w-4 mr-1 text-gray-400 inline-block"
                ),
                rx.fragment(),
            ),
            label,
            class_name="text-sm font-medium text-gray-500 flex items-center",
        ),
        rx.el.dd(
            value,
            class_name="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 font-medium",
        ),
        class_name="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b border-gray-100 last:border-0",
    )


def product_row(product) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            product["part_number"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            product["manufacturer"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            product["description"],
            class_name="px-6 py-4 text-sm text-gray-500 max-w-xs truncate",
        ),
        rx.el.td(
            f"${product['price']}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono",
        ),
        rx.el.td(
            rx.el.span(
                product["stock"],
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.button(
                "View",
                class_name="text-purple-600 hover:text-purple-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50",
    )


def vendor_detail_page() -> rx.Component:
    vendor = VendorState.active_vendor
    return layout(
        rx.el.div(
            rx.el.nav(
                rx.el.ol(
                    rx.el.li(
                        rx.el.div(
                            rx.el.a(
                                "Vendors",
                                href="/vendors",
                                class_name="text-gray-400 hover:text-gray-500 text-sm font-medium transition-colors",
                            ),
                            rx.icon(
                                "chevron-right",
                                class_name="flex-shrink-0 h-5 w-5 text-gray-300 mx-2",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.li(
                        rx.el.span(
                            vendor["name"],
                            class_name="text-sm font-medium text-purple-600",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center space-x-2",
                ),
                class_name="mb-6 border-b border-gray-200 pb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        vendor["name"], class_name="text-3xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        f"ID: {vendor['id']}", class_name="text-sm text-gray-500 mt-1"
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("pencil", class_name="h-4 w-4 mr-2"),
                        "Edit Vendor",
                        on_click=lambda: VendorState.open_edit_modal(vendor),
                        class_name="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors mr-3",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4 mr-2"),
                        "Add Product",
                        on_click=lambda: ProductState.open_add_modal_with_vendor(
                            vendor["id"]
                        ),
                        class_name="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors",
                    ),
                    class_name="mt-4 md:mt-0 flex",
                ),
                class_name="md:flex md:items-center md:justify-between mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Contact Information",
                            class_name="text-lg leading-6 font-medium text-gray-900 mb-4 px-6 pt-5",
                        ),
                        rx.el.dl(
                            detail_item("Main Contact", vendor["contact_name"], "user"),
                            detail_item("Phone", vendor["phone"], "phone"),
                            detail_item("Main Email", vendor["email"], "mail"),
                            detail_item("Address", vendor["address"], "map-pin"),
                            class_name="sm:divide-y sm:divide-gray-200",
                        ),
                        class_name="bg-white shadow overflow-hidden sm:rounded-lg h-full",
                    ),
                    class_name="col-span-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Order Settings",
                            class_name="text-lg leading-6 font-medium text-gray-900 mb-4 px-6 pt-5",
                        ),
                        rx.el.dl(
                            detail_item(
                                "Orders Email", vendor["orders_email"], "inbox"
                            ),
                            detail_item(
                                "Credit Limit",
                                f"${vendor['credit_limit']}",
                                "credit-card",
                            ),
                            detail_item(
                                "Total Orders",
                                f"{vendor['total_orders']}",
                                "shopping-cart",
                            ),
                            rx.el.div(
                                rx.el.dt(
                                    "Status",
                                    class_name="text-sm font-medium text-gray-500",
                                ),
                                rx.el.dd(
                                    rx.el.span(
                                        "Active",
                                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
                                    ),
                                    class_name="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2",
                                ),
                                class_name="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6",
                            ),
                            class_name="sm:divide-y sm:divide-gray-200",
                        ),
                        class_name="bg-white shadow overflow-hidden sm:rounded-lg h-full",
                    ),
                    class_name="col-span-1",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Vendor Products",
                    class_name="text-lg leading-6 font-medium text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Part No.",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Manufacturer",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Description",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Price",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Stock",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th("", class_name="px-6 py-3 relative"),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(ProductState.vendor_products, product_row),
                            rx.cond(
                                ProductState.vendor_products.length() == 0,
                                rx.el.tr(
                                    rx.el.td(
                                        "No products found for this vendor.",
                                        col_span=6,
                                        class_name="px-6 py-12 text-center text-sm text-gray-500 italic",
                                    )
                                ),
                                rx.fragment(),
                            ),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
                ),
                class_name="mb-12",
            ),
            vendor_modal(),
            product_modal(),
            class_name="w-full",
        )
    )