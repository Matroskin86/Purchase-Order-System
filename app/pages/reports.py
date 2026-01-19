import reflex as rx
from app.components.layout import layout
from app.states.report_state import ReportState


def stat_card(title: str, value: str, icon: str, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500 truncate"),
                rx.el.p(value, class_name="mt-1 text-3xl font-semibold text-gray-900"),
            ),
            rx.el.div(
                rx.icon(icon, class_name=f"h-8 w-8 {color_class}"),
                class_name="p-3 bg-gray-50 rounded-full",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6",
    )


def reports_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Reports & Analytics", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Overview of procurement performance.",
                    class_name="mt-1 text-sm text-gray-500",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                stat_card(
                    "Total Spend",
                    f"${ReportState.total_spend}",
                    "dollar-sign",
                    "text-green-600",
                ),
                stat_card(
                    "Total Orders",
                    ReportState.total_orders.to_string(),
                    "shopping-bag",
                    "text-purple-600",
                ),
                stat_card(
                    "Avg Order Value",
                    f"${ReportState.avg_order_value}",
                    "bar-chart-2",
                    "text-blue-600",
                ),
                stat_card(
                    "Active Vendors",
                    ReportState.total_vendors.to_string(),
                    "users",
                    "text-orange-600",
                ),
                class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Vendor Spend Distribution",
                        class_name="text-lg leading-6 font-medium text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.recharts.bar_chart(
                            rx.recharts.cartesian_grid(
                                stroke_dasharray="3 3", vertical=False
                            ),
                            rx.recharts.x_axis(data_key="name"),
                            rx.recharts.y_axis(),
                            rx.recharts.tooltip(),
                            rx.recharts.bar(
                                data_key="value",
                                name="Spend ($)",
                                fill="#805ad5",
                                radius=[4, 4, 0, 0],
                            ),
                            data=ReportState.sales_by_vendor,
                            width="100%",
                            height=300,
                        ),
                        class_name="h-80 w-full",
                    ),
                    class_name="bg-white shadow rounded-lg p-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Orders by Week",
                        class_name="text-lg leading-6 font-medium text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.recharts.area_chart(
                            rx.recharts.cartesian_grid(
                                stroke_dasharray="3 3", vertical=False
                            ),
                            rx.recharts.x_axis(data_key="name"),
                            rx.recharts.y_axis(),
                            rx.recharts.tooltip(),
                            rx.recharts.area(
                                type_="monotone",
                                data_key="orders",
                                stroke="#6b4c9a",
                                fill="#d6bcfa",
                            ),
                            data=ReportState.orders_by_week,
                            width="100%",
                            height=300,
                        ),
                        class_name="h-80 w-full",
                    ),
                    class_name="bg-white shadow rounded-lg p-6",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Spend Share",
                        class_name="text-lg leading-6 font-medium text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.recharts.pie_chart(
                            rx.recharts.pie(
                                data=ReportState.sales_by_vendor,
                                data_key="value",
                                name_key="name",
                                cx="50%",
                                cy="50%",
                                outer_radius=100,
                                fill="#8884d8",
                                label=True,
                                stroke="#fff",
                                stroke_width=2,
                            ),
                            rx.recharts.tooltip(),
                            width="100%",
                            height=300,
                        ),
                        class_name="h-80 w-full flex justify-center",
                    ),
                    class_name="bg-white shadow rounded-lg p-6",
                ),
                class_name="grid grid-cols-1 gap-8",
            ),
            class_name="w-full",
        )
    )