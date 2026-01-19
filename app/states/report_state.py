import reflex as rx
from collections import defaultdict
from datetime import datetime
import logging
from app.states.order_state import OrderState
from app.states.vendor_state import VendorState


class ReportState(rx.State):
    """State for calculating report analytics and metrics."""

    @rx.var
    async def total_orders(self) -> int:
        orders = await self.get_state(OrderState)
        return len(orders.orders)

    @rx.var
    async def total_spend(self) -> float:
        orders = await self.get_state(OrderState)
        return sum((o["total_amount"] for o in orders.orders))

    @rx.var
    async def avg_order_value(self) -> float:
        count = await self.total_orders
        spend = await self.total_spend
        return round(spend / count, 2) if count > 0 else 0.0

    @rx.var
    async def total_vendors(self) -> int:
        vendors = await self.get_state(VendorState)
        return len(vendors.vendors)

    @rx.var
    async def sales_by_vendor(self) -> list[dict[str, str | float]]:
        orders_state = await self.get_state(OrderState)
        vendors_state = await self.get_state(VendorState)
        vendor_map = {v["id"]: v["name"] for v in vendors_state.vendors}
        sales = defaultdict(float)
        for o in orders_state.orders:
            v_name = vendor_map.get(o["vendor_id"], "Unknown")
            sales[v_name] += o["total_amount"]
        return [{"name": name, "value": round(val, 2)} for name, val in sales.items()]

    @rx.var
    async def orders_by_week(self) -> list[dict[str, str | int]]:
        orders_state = await self.get_state(OrderState)
        weeks = defaultdict(int)
        for o in orders_state.orders:
            try:
                dt = datetime.strptime(o["date"], "%Y-%m-%d %H:%M:%S")
                week_str = f"W{dt.isocalendar()[1]}"
                weeks[week_str] += 1
            except Exception as e:
                logging.exception(f"Error processing order date: {e}")
        sorted_weeks = sorted(weeks.items())
        return [{"name": k, "orders": v} for k, v in sorted_weeks]