from ns_portal.core.resources import (
    MetaEndPointResource
)
from pyramid.security import (
    Allow,
    Everyone,
    forget
)



class LogoutResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Everyone, 'read')
        ]

    def GET(self):
        forget(self.request)

        return self.request.response
