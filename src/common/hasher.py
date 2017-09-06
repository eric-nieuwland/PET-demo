import hmac
import hashlib
import base64


DEFAULT_HASH_KEY = b'1234567890'


def _number_to_bytes(number):
    """
    turn the absolute value of a number into bytes
    :param number: numeric value
    :return: bytes
    """
    rest = int(abs(number))
    if rest == 0:
        return b'\x00'

    parts = []
    while rest > 0:
        parts.append(rest & 0xff)
        rest >>= 8
    parts.reverse()
    return bytes(parts)


def make_hash(message, key=None):
    """
    transform a message into a hash - optionally with a key
    :param message: message to hash
    :param key: optional key
    :return: base64 encoded hash value
    """
    if key is None:
        key_ = DEFAULT_HASH_KEY
    elif isinstance(key, bytes):
        key_ = key
    elif isinstance(key, str):
        key_ = key.encode()
    elif isinstance(key, int):
        key_ = _number_to_bytes(key)
    else:
        raise TypeError(f"key should be bytes, str, or int, not {key.__class__.__name__}")

    if isinstance(message, str):
        msg_ = message.encode()
    elif isinstance(message, bytes):
        msg_ = message
    else:
        raise TypeError(f"message should be bytes or str, not {message.__class__.__name__}")

    # take digest, i.e. the hash result
    dig = hmac.new(key_, msg=msg_, digestmod=hashlib.sha256).digest()
    # convert the digest to a base64 encoded string and drop the superfluous final '='
    dig_base64 = base64.b64encode(dig).decode()[:-1]

    return dig_base64


def make_id_hash(id_, key=None):
    """
    transform an id (i.e. integer) into a hash  - optionally with a key
    :param id_: id to hash
    :param key: optional key
    :return: base64 encoded hash value
    """
    return make_hash(_number_to_bytes(id_), key)
