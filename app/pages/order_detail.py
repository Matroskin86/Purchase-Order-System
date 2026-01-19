import reflex as rx
from app.components.layout import layout
from app.states.order_state import OrderState
from app.states.product_state import ProductState
from app.states.auth_state import AuthState
from app.pages.orders import status_badge


def add_item_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-gray-500/75 transition-opacity z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.h3(
                        "Add Line Item",
                        class_name="text-lg leading-6 font-medium text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Select Product",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Choose a product...", value=""),
                            rx.foreach(
                                ProductState.products,
                                lambda p: rx.el.option(
                                    f"{p['part_number']} - {p['description']} (${p['price']})",
                                    value=p["id"],
                                ),
                            ),
                            on_change=OrderState.set_new_item_product,
                            class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md appearance-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Quantity",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            min="1",
                            default_value="1",
                            on_change=OrderState.set_new_item_quantity,
                            class_name="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm",
                            )
                        ),
                        rx.el.button(
                            "Add Item",
                            on_click=OrderState.add_line_item,
                            class_name="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm",
                        ),
                        class_name="flex flex-col sm:flex-row-reverse",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg z-50",
            ),
        ),
        open=OrderState.is_add_item_modal_open,
        on_open_change=OrderState.set_is_add_item_modal_open,
    )


def line_item_row(item: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            item["product_id"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            f"${item['unit_price']}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            item["quantity"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            f"${item['total_price']}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono",
        ),
        rx.el.td(
            rx.cond(
                OrderState.current_order["status"] == "Pending",
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=OrderState.remove_line_item(item["id"]),
                    class_name="text-red-400 hover:text-red-600 transition-colors",
                ),
                rx.fragment(),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def order_detail_page() -> rx.Component:
    order = OrderState.current_order
    return layout(
        rx.el.div(
            rx.el.nav(
                rx.el.ol(
                    rx.el.li(
                        rx.el.a(
                            "Orders",
                            href="/orders",
                            class_name="text-sm font-medium text-gray-500 hover:text-gray-700 transition-colors",
                        ),
                        class_name="inline-flex items-center",
                    ),
                    rx.el.li(
                        rx.icon(
                            "chevron-right",
                            class_name="flex-shrink-0 h-4 w-4 text-gray-400 mx-2",
                        ),
                        class_name="inline-flex items-center",
                    ),
                    rx.el.li(
                        rx.el.span(
                            f"Order #{order['id']}",
                            class_name="text-sm font-medium text-gray-900",
                        ),
                        class_name="inline-flex items-center",
                    ),
                    class_name="flex items-center",
                ),
                class_name="mb-8 flex",
                aria_label="Breadcrumb",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h1(
                                f"Order #{order['id']}",
                                class_name="text-2xl font-bold text-gray-900 sm:text-3xl tracking-tight",
                            ),
                            rx.el.div(
                                status_badge(order["status"]),
                                class_name="ml-4 flex items-center self-center",
                            ),
                            class_name="flex flex-row items-center",
                        ),
                        rx.el.div(
                            rx.el.span("Created on", class_name="text-gray-500 mr-1"),
                            rx.el.span(
                                order["date"], class_name="font-medium text-gray-900"
                            ),
                            class_name="mt-2 text-sm flex items-center",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.cond(
                            (order["status"] == "Pending") & AuthState.is_admin,
                            rx.el.div(
                                rx.el.button(
                                    "Reject",
                                    on_click=lambda: OrderState.update_status(
                                        "Rejected"
                                    ),
                                    class_name="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors mr-3",
                                ),
                                rx.el.button(
                                    "Approve",
                                    on_click=lambda: OrderState.update_status(
                                        "Approved"
                                    ),
                                    class_name="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors",
                                ),
                                class_name="flex",
                            ),
                            rx.fragment(),
                        ),
                        class_name="mt-4 md:mt-0 md:ml-4 flex-shrink-0",
                    ),
                    class_name="md:flex md:items-center md:justify-between",
                ),
                class_name="bg-white shadow-sm border border-gray-200 rounded-lg px-4 py-5 sm:px-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.dl(
                        rx.el.div(
                            rx.el.dt(
                                "Order Date",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                order["date"], class_name="mt-1 text-sm text-gray-900"
                            ),
                            class_name="sm:col-span-1",
                        ),
                        rx.el.div(
                            rx.el.dt(
                                "Ordered By",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                order["created_by_user_id"],
                                class_name="mt-1 text-sm text-gray-900",
                            ),
                            class_name="sm:col-span-1",
                        ),
                        rx.el.div(
                            rx.el.dt(
                                "Vendor ID",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                order["vendor_id"],
                                class_name="mt-1 text-sm text-gray-900",
                            ),
                            class_name="sm:col-span-1",
                        ),
                        rx.el.div(
                            rx.el.dt(
                                "Total Amount",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.dd(
                                f"${order['total_amount']}",
                                class_name="mt-1 text-2xl font-bold text-gray-900",
                            ),
                            class_name="sm:col-span-1",
                        ),
                        class_name="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-4",
                    ),
                    class_name="bg-white shadow rounded-lg px-4 py-5 sm:p-6 mb-8",
                )
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Line Items",
                        class_name="text-lg leading-6 font-medium text-gray-900",
                    ),
                    rx.cond(
                        order["status"] == "Pending",
                        rx.el.button(
                            rx.icon("plus", class_name="h-4 w-4 mr-2"),
                            "Add Item",
                            on_click=OrderState.open_add_item_modal,
                            class_name="inline-flex items-center px-3 py-1.5 border border-transparent rounded-md text-sm font-medium text-purple-700 bg-purple-100 hover:bg-purple-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Product ID",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Unit Price",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Qty",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Total",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th("", class_name="px-6 py-3 relative"),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(OrderState.current_order_lines, line_item_row),
                            rx.cond(
                                OrderState.current_order_lines.length() == 0,
                                rx.el.tr(
                                    rx.el.td(
                                        "No line items yet.",
                                        col_span=5,
                                        class_name="px-6 py-4 text-center text-sm text-gray-500 italic",
                                    )
                                ),
                                rx.fragment(),
                            ),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        rx.el.tfoot(
                            rx.el.tr(
                                rx.el.td(
                                    "Total",
                                    col_span=3,
                                    class_name="px-6 py-4 text-right text-sm font-medium text-gray-900",
                                ),
                                rx.el.td(
                                    f"${order['total_amount']}",
                                    class_name="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900",
                                ),
                                rx.el.td("", class_name="px-6 py-4"),
                                class_name="bg-gray-50",
                            )
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
                ),
            ),
            add_item_modal(),
            class_name="w-full",
        )
    )