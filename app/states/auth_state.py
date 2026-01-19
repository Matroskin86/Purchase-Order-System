import reflex as rx
from typing import Optional
from app.states.models import User


class AuthState(rx.State):
    """Manages the current logged-in user."""

    current_user: User = {
        "id": "u1",
        "name": "Jane Admin",
        "email": "jane@company.com",
        "role": "Admin",
        "avatar_url": "https://api.dicebear.com/9.x/notionists/svg?seed=Jane",
    }
    is_logged_in: bool = True

    @rx.var
    def is_admin(self) -> bool:
        return self.current_user["role"] == "Admin"

    @rx.event
    def logout(self):
        self.is_logged_in = False
        return rx.redirect("/")

    @rx.event
    def login(self):
        self.is_logged_in = True