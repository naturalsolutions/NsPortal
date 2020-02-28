from .metarootresource import (
    MetaRootResource,
    MetaCollectionResource,
    MetaEmptyResource,
    MetaEndPointResource
)
from .restviews import (
    IRESTview
)

__all__ = [
    "MetaRootResource",
    "MetaCollectionResource",
    "MetaEmptyResource",
    "MetaEndPointResource",
    "IRESTview"
]


def includeme(config):
    config.scan('.restviews')
