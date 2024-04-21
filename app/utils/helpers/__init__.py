import random, string
from .basic_helpers import check_emerge, console_log, log_exception

def generate_random_string(length):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))