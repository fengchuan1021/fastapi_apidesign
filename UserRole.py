from enum import Enum

class UserRole(Enum):
    customer=0
    admin=1<<1