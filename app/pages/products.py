import reflex as rx
from app.components.layout import layout
from app.states.product_state import ProductState
from app.components.product_form import product_modal


def product_table_row(product) -> rx.Component:
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
            rx.el.div(
                rx.el.button(
                    "Edit",
                    on_click=lambda: ProductState.open_edit_modal(product),
                    class_name="text-purple-600 hover:text-purple-900 font-medium text-sm mr-4",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=ProductState.delete_product(product["id"]),
                    class_name="text-red-400 hover:text-red-600 transition-colors",
                ),
                class_name="flex items-center justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-0",
    )


def products_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Products", class_name="text-2xl font-bold text-gray-900"),
                    rx.el.p(
                        "Manage catalog of parts and items.",
                        class_name="mt-1 text-sm text-gray-500",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-5 w-5 mr-2"),
                    "Add Product",
                    on_click=ProductState.open_add_modal,
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
                            placeholder="Search products by part no, desc...",
                            on_change=ProductState.set_search,
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
                            rx.foreach(
                                ProductState.filtered_products, product_table_row
                            ),
                            rx.cond(
                                ProductState.filtered_products.length() == 0,
                                rx.el.tr(
                                    rx.el.td(
                                        "No products found.",
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
                class_name="flex flex-col",
            ),
            product_modal(),
            class_name="w-full",
        )
    )