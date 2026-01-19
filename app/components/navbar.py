import reflex as rx
from app.states.auth_state import AuthState


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.el.a(
        text,
        href=url,
        class_name="text-gray-100 hover:text-white hover:bg-white/10 px-3 py-2 rounded-md text-sm font-medium transition-colors",
    )


def user_menu() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=AuthState.current_user["avatar_url"],
                class_name="h-8 w-8 rounded-full border-2 border-purple-300",
            ),
            rx.el.div(
                rx.el.p(
                    AuthState.current_user["name"],
                    class_name="text-sm font-medium text-white leading-none",
                ),
                rx.el.p(
                    AuthState.current_user["role"],
                    class_name="text-xs text-purple-200 mt-1 leading-none",
                ),
                class_name="hidden md:block",
            ),
            class_name="flex items-center gap-3",
        ),
        class_name="ml-4",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("package", class_name="h-8 w-8 text-white mr-3"),
                        rx.el.span(
                            "ProcureFlow",
                            class_name="text-white text-xl font-bold tracking-tight",
                        ),
                        class_name="flex-shrink-0 flex items-center",
                    ),
                    rx.el.div(
                        rx.el.div(
                            navbar_link("Vendors", "/vendors"),
                            navbar_link("Products", "/products"),
                            navbar_link("Orders", "/orders"),
                            navbar_link("Reports", "/reports"),
                            class_name="ml-10 flex items-baseline space-x-4",
                        ),
                        class_name="hidden md:block",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(user_menu(), class_name="hidden md:block"),
                rx.el.div(
                    rx.el.button(
                        rx.icon("menu", class_name="h-6 w-6 text-white"),
                        class_name="bg-purple-700 inline-flex items-center justify-center p-2 rounded-md text-gray-200 hover:text-white hover:bg-purple-600 focus:outline-none",
                    ),
                    class_name="-mr-2 flex md:hidden",
                ),
                class_name="flex items-center justify-between h-16",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="bg-[#6b4c9a] shadow-md",
    )