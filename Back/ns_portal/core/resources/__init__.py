from .metarootresource import (
    MetaRootResource,
    MetaCollectionRessource,
    MetaEmptyRessource
)
from .restviews import (
    IRESTview
)

__all__ = [
    "MetaRootResource",
    "MetaCollectionRessource",
    "MetaEmptyRessource",
    "IRESTview"
]


def includeme(config):
    config.scan('.restviews')
