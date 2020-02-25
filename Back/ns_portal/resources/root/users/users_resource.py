from ns_portal.core.resources import (
    MetaEndPointResource
)
from ns_portal.database.main_db import (
    TUsers
)
from pyramid.security import (
    Allow,
    Everyone
)


class UsersResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Everyone, 'read')
        ]

    def GET(self):
        query = self.request.dbsession.query(
            TUsers.TUse_Login.label('fullname')
            )
        query = query.filter(TUsers.TUse_HasAccess == 1)
        query = query.order_by(TUsers.TUse_Login)
        res = query.all()

        self.request.response.json_body = [row._asdict() for row in res]
        return self.request.response
