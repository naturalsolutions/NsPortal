from .token import (
    getOauth2CodeWithSecret,
    getToken,
    checkOauth2CodeAndGiveToken,
    myDecode
)

__all__ = [
    "getOauth2CodeWithSecret",
    "getToken",
    "checkOauth2CodeAndGiveToken",
    "myDecode"
]


def includeme(config):
    config.scan('.errors_views')
