from ns_portal.core.resources import (
    MetaEmptyRessource
)
from .authorize import (
    AuthorizeResource
)
from .login import (
    LoginResource
)
from .logout import (
    LogoutResource
)
from .token import (
    TokenResource
)


class VersionResource(MetaEmptyRessource):
    __ROUTES__ = {
        'authorize': AuthorizeResource,
        'login': LoginResource,
        'logout': LogoutResource,
        'token': TokenResource,
    }
