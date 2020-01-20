from .security_resource import (
    SecurityResource
)

__all__ = [
    "SecurityResource"
]


def includeme(config):
    config.scan('.security_views')
