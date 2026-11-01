from collections import namedtuple
from dataclasses import dataclass

user = namedtuple("user", "username, login, password, date")
new_user = user("john", "ojt", "1234", "12-04-2026")
#print(new_user.password)

@dataclass
class Accessories:
    book: str
    calc: int
    time: float

my_accessories = Accessories("text", "64", 12.3)
print(my_accessories.calc)
