from .resources import (
    MetaRootResource,
    MetaCollectionResource,
    MetaEmptyResource,
    IRESTview
)

__all__ = [
    "MetaRootResource",
    "MetaCollectionResource",
    "MetaEmptyResource",
    "IRESTview"

]


def includeme(config):
    config.add('.resources')
