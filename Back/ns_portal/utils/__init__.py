from .token import (
    myDecode,
    getCookieToken,
    getCodeToken,
    getAccessToken,
    getRefreshToken
)

__all__ = [
    "myDecode",
    "getCookieToken",
    "getCodeToken",
    "getAccessToken",
    "getRefreshToken"
]


def includeme(config):
    config.scan('.errors_views')
