from .metarootresource import (
    MetaRootResource,
    MetaCollectionRessource,
    MetaEmptyRessource,
    MetaEndPointResource
)
from .restviews import (
    IRESTview
)

__all__ = [
    "MetaRootResource",
    "MetaCollectionRessource",
    "MetaEmptyRessource",
    "MetaEndPointResource",
    "IRESTview"
]


def includeme(config):
    config.scan('.restviews')
