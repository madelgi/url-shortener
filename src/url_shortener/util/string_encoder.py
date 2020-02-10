import base64


ALTCHARS = b'-_'


def base64_encode(_id: int):
    """Encode a positive number in Base 64

    Arguments:
        s: The string to encode
    """
    return base64.b64encode(f"{str(_id)}".encode(), ALTCHARS)


def base64_decode(encoded: str):
    """Decode a Base X encoded string into the number

    Arguments:
        encoded: The encoded string
    """
    return base64.b64decode(encoded, ALTCHARS).decode()
