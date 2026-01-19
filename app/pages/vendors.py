import reflex as rx
from app.components.layout import layout
from app.states.vendor_state import VendorState
from app.components.vendor_form import vendor_modal


def vendor_row(vendor) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(vendor["name"], class_name="text-sm font-medium text-gray-900"),
                rx.el.p(vendor["email"], class_name="text-sm text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(vendor["contact_name"], class_name="text-sm text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(vendor["phone"], class_name="text-sm text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"${vendor['credit_limit']}",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "View",
                    on_click=VendorState.navigate_to_vendor(vendor["id"]),
                    class_name="text-purple-600 hover:text-purple-900 font-medium text-sm mr-4",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=VendorState.delete_vendor(vendor["id"]),
                    class_name="text-red-400 hover:text-red-600 transition-colors",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-0",
    )


def vendors_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Vendors", class_name="text-2xl font-bold text-gray-900"),
                    rx.el.p(
                        "Manage your supplier relationships and contacts.",
                        class_name="mt-1 text-sm text-gray-500",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-5 w-5 mr-2"),
                    "Add Vendor",
                    on_click=VendorState.open_add_modal,
                    class_name="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors",
                ),
                class_name="md:flex md:items-center md:justify-between mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Search vendors...",
                            on_change=VendorState.set_search,
                            class_name="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-purple-500 focus:border-purple-500 sm:text-sm",
                        ),
                        class_name="relative rounded-md shadow-sm max-w-md",
                    )
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Vendor",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Main Contact",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Phone",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Credit Limit",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(VendorState.filtered_vendors, vendor_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
                ),
                class_name="flex flex-col",
            ),
            vendor_modal(),
            class_name="w-full",
        )
    )