import requests


class EscapeSecs:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"


def make_request(url: str) -> requests.Response:
    try:
        response = requests.get(url, timeout=10)
    except (
        requests.exceptions.HTTPerror,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.Requestexception,
    ) as e:
        raise e

    return response
