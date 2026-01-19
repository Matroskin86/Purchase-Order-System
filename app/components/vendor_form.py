import reflex as rx
from app.states.vendor_state import VendorState


def form_field(
    label: str,
    field_name: str,
    value_state: rx.Var,
    type_: str = "text",
    placeholder: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            default_value=value_state,
            placeholder=placeholder,
            on_change=lambda val: VendorState.update_form_field(field_name, val),
            class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm",
        ),
        class_name="mb-4",
    )


def credit_field() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Credit Limit ($)",
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        rx.el.input(
            type="number",
            default_value=VendorState.form_credit.to_string(),
            on_change=VendorState.update_credit_field,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm",
        ),
        class_name="mb-4",
    )


def vendor_modal() -> rx.Component:
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
                                VendorState.editing_vendor_id != "",
                                "Edit Vendor",
                                "Add New Vendor",
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
                        form_field(
                            "Company Name",
                            "name",
                            VendorState.form_name,
                            placeholder="e.g. Acme Corp",
                        ),
                        rx.el.div(
                            form_field(
                                "Contact Person",
                                "contact",
                                VendorState.form_contact,
                                placeholder="John Doe",
                            ),
                            form_field(
                                "Phone",
                                "phone",
                                VendorState.form_phone,
                                type_="tel",
                                placeholder="(555) 555-5555",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                        ),
                        rx.el.div(
                            form_field(
                                "Main Email",
                                "email",
                                VendorState.form_email,
                                type_="email",
                                placeholder="info@vendor.com",
                            ),
                            form_field(
                                "Orders Email",
                                "orders_email",
                                VendorState.form_orders_email,
                                type_="email",
                                placeholder="orders@vendor.com",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                        ),
                        form_field(
                            "Address",
                            "address",
                            VendorState.form_address,
                            placeholder="123 Street, City, State, Zip",
                        ),
                        credit_field(),
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
                                VendorState.editing_vendor_id != "",
                                "Save Changes",
                                "Create Vendor",
                            ),
                            on_click=VendorState.save_vendor,
                            class_name="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm",
                        ),
                        class_name="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse -mx-6 -mb-6 mt-6 rounded-b-lg border-t border-gray-200",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg z-50",
            ),
        ),
        open=VendorState.is_modal_open,
        on_open_change=VendorState.set_is_modal_open,
    )