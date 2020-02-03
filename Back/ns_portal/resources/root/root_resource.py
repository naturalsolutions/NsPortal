from ns_portal.core.resources import (
    MetaRootResource
)
from .security import (
    SecurityResource
)
from .site import (
    SiteResource
)
from .me import (
    MeResource
)


class MyRoot(MetaRootResource):

    __ROUTES__ = {
        'security':  SecurityResource,
        'site': SiteResource,
        'me': MeResource
    }
