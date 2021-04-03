import random
from string import ascii_lowercase, ascii_uppercase, digits

import names

from app.models.user import User


def generate_random_password() -> str:
    """
    return: string with random three uppercase,three lowercase and three digits in shuffled order
    """
    return "".join(
        random.sample(
            random.choices(ascii_lowercase, k=3)
            + random.choices(ascii_uppercase, k=3)
            + random.choices(digits, k=3),
            9,
        )
    )


def generate_random_fullname() -> str:
    return names.get_full_name()


def generate_random_email() -> str:
    return "".join(
        "".join(random.choices(ascii_lowercase, k=15))
        + "@"
        + "".join(random.choices(ascii_lowercase, k=10))
        + ".com"
    )


def generate_random_phone_number() -> str:
    return "".join(random.choice(["6", "7", "8", "9"])) + "".join(
        random.choices(digits, k=9)
    )


def generate_random_user_document(is_admin: bool, is_active: bool) -> User:
    return User(
        fullname=generate_random_fullname(),
        email=generate_random_email(),
        phone=generate_random_phone_number(),
        is_admin=is_admin,
        password=generate_random_password(),
        is_active=is_active,
    )
