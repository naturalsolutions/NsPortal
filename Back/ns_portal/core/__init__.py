from .resources import (
    MetaRootResource,
    MetaCollectionRessource,
    MetaEmptyRessource,
    IRESTview
)

__all__ = [
    "MetaRootResource",
    "MetaCollectionRessource",
    "MetaEmptyRessource",
    "IRESTview"

]


def includeme(config):
    config.add('.resources')
