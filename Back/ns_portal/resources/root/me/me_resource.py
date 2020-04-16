from ns_portal.core.resources import (
    MetaEndPointResource
)
from pyramid.security import (
    Allow,
    Authenticated
)


class MeResource(MetaEndPointResource):
    __acl__ = [
        (Allow, Authenticated, 'read')
        ]

    def GET(self):
        return self.request.authenticated_userid
