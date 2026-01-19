import reflex as rx
from app.states.product_state import ProductState
from app.states.vendor_state import VendorState


def product_form_field(
    label: str,
    field_name: str,
    value_state: rx.Var,
    type_: str = "text",
    placeholder: str = "",
    is_number: bool = False,
) -> rx.Component:
    if field_name == "price":
        on_change_handler = ProductState.update_price
    elif field_name == "stock":
        on_change_handler = ProductState.update_stock
    else:
        on_change_handler = lambda val: ProductState.update_form_field(field_name, val)
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            default_value=value_state.to_string(),
            placeholder=placeholder,
            on_change=on_change_handler,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm",
        ),
        class_name="mb-4",
    )


def product_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-gray-500/75 transition-opacity z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            rx.cond(
                                ProductState.editing_product_id != "",
                                "Edit Product",
                                "Add New Product",
                            ),
                            class_name="text-lg leading-6 font-medium text-gray-900",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="h-5 w-5 text-gray-400"),
                                class_name="bg-white rounded-md hover:text-gray-500 focus:outline-none",
                            )
                        ),
                        class_name="flex justify-between items-center mb-5 pb-3 border-b border-gray-200",
                    ),
                    rx.el.div(
                        rx.el.div(
                            product_form_field(
                                "Part Number",
                                "part_number",
                                ProductState.form_part_number,
                                placeholder="e.g. A-123",
                            ),
                            product_form_field(
                                "Manufacturer",
                                "manufacturer",
                                ProductState.form_manufacturer,
                                placeholder="Acme Corp",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                        ),
                        product_form_field(
                            "Description",
                            "description",
                            ProductState.form_description,
                            placeholder="Product description",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Vendor",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Select Vendor", value=""),
                                rx.foreach(
                                    VendorState.vendors,
                                    lambda vendor: rx.el.option(
                                        vendor["name"], value=vendor["id"]
                                    ),
                                ),
                                value=ProductState.form_vendor_id,
                                on_change=lambda val: ProductState.update_form_field(
                                    "vendor_id", val
                                ),
                                class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md mb-4 appearance-none",
                            ),
                        ),
                        rx.el.div(
                            product_form_field(
                                "Price ($)",
                                "price",
                                ProductState.form_price,
                                type_="number",
                            ),
                            product_form_field(
                                "Initial Stock",
                                "stock",
                                ProductState.form_stock,
                                type_="number",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                        ),
                        class_name="space-y-1",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm",
                            )
                        ),
                        rx.el.button(
                            rx.cond(
                                ProductState.editing_product_id != "",
                                "Save Changes",
                                "Create Product",
                            ),
                            on_click=ProductState.save_product,
                            class_name="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm",
                        ),
                        class_name="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse -mx-6 -mb-6 mt-6 rounded-b-lg border-t border-gray-200",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg z-50",
            ),
        ),
        open=ProductState.is_modal_open,
        on_open_change=ProductState.set_is_modal_open,
    )