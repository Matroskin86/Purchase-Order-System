import reflex as rx
from app.components.navbar import navbar


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            content,
            class_name="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 bg-gray-50 min-h-[calc(100vh-64px)]",
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )