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
from .users import (
    UsersResource
)
from .instances import (
    InstancesResource
)


class MyRoot(MetaRootResource):

    __ROUTES__ = {
        'security':  SecurityResource,
        'site': SiteResource,
        'me': MeResource,
        'user': UsersResource,
        'instance': InstancesResource
    }
