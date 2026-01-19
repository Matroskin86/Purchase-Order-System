import reflex as rx
from app.components.layout import layout
from app.states.order_state import OrderState
from app.states.vendor_state import VendorState


def create_order_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-gray-500/75 transition-opacity z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.h3(
                        "Create New Purchase Order",
                        class_name="text-lg leading-6 font-medium text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Select Vendor",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Choose a vendor...", value=""),
                            rx.foreach(
                                VendorState.vendors,
                                lambda vendor: rx.el.option(
                                    vendor["name"], value=vendor["id"]
                                ),
                            ),
                            on_change=OrderState.set_new_order_vendor,
                            class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md appearance-none",
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
                            "Create Order",
                            on_click=OrderState.create_order,
                            class_name="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm",
                        ),
                        class_name="flex flex-col sm:flex-row-reverse",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-sm sm:w-full sm:p-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-sm z-50",
            ),
        ),
        open=OrderState.is_create_modal_open,
        on_open_change=OrderState.set_is_create_modal_open,
    )


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Approved",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
            (
                "Rejected",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
            (
                "Pending",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def order_row(order) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.moment(order["date"], format="MM/DD/YYYY hh:mm a"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.span(order["id"], class_name="font-medium text-purple-600"),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            order["created_by_user_id"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            status_badge(order["status"]),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            f"${order['total_amount']}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono",
        ),
        rx.el.td(
            rx.el.a(
                "View",
                href=f"/orders/{order['id']}",
                class_name="text-purple-600 hover:text-purple-900 font-medium text-sm",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors duration-150",
    )


def orders_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Purchase Orders", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Track and manage purchase orders.",
                        class_name="mt-1 text-sm text-gray-500",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-5 w-5 mr-2"),
                    "Add Purchase Order",
                    on_click=OrderState.open_create_modal,
                    class_name="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors",
                ),
                class_name="md:flex md:items-center md:justify-between mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Date",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "PO Number",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Ordered By",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
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
                            rx.foreach(OrderState.paginated_orders, order_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Showing page ",
                            rx.el.span(OrderState.page, class_name="font-medium"),
                            " of ",
                            rx.el.span(
                                OrderState.total_pages, class_name="font-medium"
                            ),
                            class_name="text-sm text-gray-700",
                        )
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("chevron-left", class_name="h-5 w-5"),
                            on_click=OrderState.prev_page,
                            disabled=OrderState.page == 1,
                            class_name="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        rx.el.button(
                            rx.icon("chevron-right", class_name="h-5 w-5"),
                            on_click=OrderState.next_page,
                            disabled=OrderState.page == OrderState.total_pages,
                            class_name="-ml-px relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        class_name="relative z-0 inline-flex shadow-sm rounded-md",
                    ),
                    class_name="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-4 rounded-lg shadow",
                ),
                class_name="flex flex-col",
            ),
            create_order_modal(),
            class_name="w-full",
        )
    )