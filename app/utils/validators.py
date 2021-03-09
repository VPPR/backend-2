def is_phone_valid(phone: str) -> bool:
    if (
        phone.isnumeric()
        and phone.startswith(("6", "7", "8", "9"))
        and len(phone) == 10
    ):
        return True
    return False
