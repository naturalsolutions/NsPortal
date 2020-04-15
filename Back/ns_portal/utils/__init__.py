from .token import (
    myDecode,
    getCookieToken,
    getCodeToken,
    getAccessToken,
    getRefreshToken
)
from .utils import (
    my_get_authentication_policy
)

__all__ = [
    "myDecode",
    "getCookieToken",
    "getCodeToken",
    "getAccessToken",
    "getRefreshToken",
    "my_get_authentication_policy"
]


def includeme(config):
    config.scan('.errors_views')
