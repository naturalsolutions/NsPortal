from ns_portal.core.resources import (
    MetaEmptyResource
)
from .v1 import (
    VersionResource
)


class OAuth2Resource(MetaEmptyResource):
    __ROUTES__ = {
        'v1': VersionResource
    }
