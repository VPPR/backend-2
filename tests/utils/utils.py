import random
from string import ascii_lowercase, ascii_uppercase, digits

def get_random_password() -> str:
    """
    return: string with random three uppercase,three lowercase and three digits in shuffled order
    """
    return "".join(random.sample(
       random.choices(ascii_lowercase, k=3) + random.choices(ascii_uppercase, k=3) + random.choices(digits, k=3), 9
    ))