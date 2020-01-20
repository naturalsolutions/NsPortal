from ns_portal.core.resources import (
    MetaRootResource
)
from ns_portal.resources.security import (
    SecurityResource
)


class MyRoot(MetaRootResource):
    __ROUTES__ = {
        'security':  SecurityResource,
    }
