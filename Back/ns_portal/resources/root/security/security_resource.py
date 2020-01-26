from ns_portal.core.resources import (
    MetaRootResource
)
from .oauth2 import (
    OAuth2Resource
)


class SecurityResource(MetaRootResource):

    __ROUTES__ = {
        'oauth2': OAuth2Resource
    }
