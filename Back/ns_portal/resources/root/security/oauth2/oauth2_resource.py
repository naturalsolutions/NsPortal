from ns_portal.core.resources import (
    MetaEmptyRessource
)
from .v1 import (
    VersionResource
)


class OAuth2Resource(MetaEmptyRessource):
    __ROUTES__ = {
        'v1': VersionResource
    }
