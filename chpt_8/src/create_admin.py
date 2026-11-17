import getpass
import sys
from data.error import Duplicate
from data.db import get_db_cm, init_db
from model.user import UserCreate
from service import user as service


def main() -> None:
    init_db()
    name = input("Admin username: ").strip()
    password = getpass.getpass(
        "Password (8 to 128 characters): "
    )  # not echoed to the screen
    new = UserCreate(name=name, password=password)
    try:
        with get_db_cm() as db:
            service.create(db, new, role="admin")
    except Duplicate:
        sys.exit(f"User {name} already exists")
    print(f"Admin {name} created")


if __name__ == "__main__":
    main()
