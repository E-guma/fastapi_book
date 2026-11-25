"""Create the initial administrator account on startup."""

from config import ADMIN_PASSWORD, ADMIN_USERNAME
from data.db import get_db_cm
from data.error import Duplicate
from model.user import UserCreate
from pydantic import ValidationError
from service import user as service


def set_admin() -> None:
    """Ensure an admin account exists, creating one from environment config.

    Skips when any admin is already present. ``ADMIN_PASSWORD`` is required
    only when an admin must be created; ``ADMIN_USERNAME`` defaults to
    ``admin``.
    """
    name = ADMIN_USERNAME.strip()
    password = ADMIN_PASSWORD

    with get_db_cm() as session:
        if any(user.role == "admin" for user in service.get_all(session)):
            return

        if not password:
            raise RuntimeError("ADMIN_PASSWORD environment variable is not set")
        if not name:
            raise RuntimeError("ADMIN_USERNAME environment variable is empty")

        try:
            new_admin = UserCreate(name=name, password=password)
        except ValidationError as exc:
            raise RuntimeError(f"Invalid admin configuration: {exc}") from exc

        try:
            service.create(session, new_admin, role="admin")
        except Duplicate as exc:
            raise RuntimeError(
                f"User {name} already exists but is not an admin"
            ) from exc
