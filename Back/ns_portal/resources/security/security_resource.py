from ns_portal.core.resources import (
    MetaRootResource,
    MetaEmptyRessource
)
from .security_views import (
    ISECURITYview
)
from zope.interface import implementer


@implementer(ISECURITYview)
class VersionResource(MetaEmptyRessource):
    pass


class OAuth2Resource(MetaEmptyRessource):
    __ROUTES__ = {
        'v2': VersionResource
    }


class SecurityResource(MetaRootResource):

    __ROUTES__ = {
        'oauth2': OAuth2Resource
    }
