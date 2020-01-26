from ns_portal.core.resources import (
    MetaRootResource
)
from .security import (
    SecurityResource
)


class MyRoot(MetaRootResource):
    __ROUTES__ = {
        'security':  SecurityResource,
    }
