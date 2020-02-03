from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    ValidationError
)
from pyramid.security import (
    Allow,
    Authenticated
)
from ns_portal.database.main_db import (
    TApplications
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound
)
from ns_portal.utils import (
    getOauth2CodeWithSecret
)


class authorizeSchema(Schema):
    client_id = fields.String(required=True)
    redirect_uri = fields.String(required=True)


class AuthorizeResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Authenticated, 'create')
    ]

    def validateSchema(self, data):
        client_id = data.get('client_id')
        redirect_uri = data.get('redirect_uri')

        query = self.request.dbsession.query(TApplications)
        query = query.filter(
            TApplications.TApp_Name == client_id,
            TApplications.TApp_Name.like(f'%{redirect_uri}%')
            )
        try:
            res = query.one_or_none()
        except MultipleResultsFound:
            raise MultipleResultsFound()
        if res:
            return True
        else:
            raise ValidationError({
                "error": (
                    f'your client_id and/or redirect_uri'
                    f' are wrongs'
                    )
                })

    def POST(self):
        reqParams = self.__parser__(
            args=authorizeSchema(),
            location='json'
        )

        self.validateSchema(data=reqParams)

        code = getOauth2CodeWithSecret(
            idUser=self.request.authenticated_userid.get('TUse_PK_ID'),
            client_id=reqParams.get('client_id'),
            request=self.request
        )

        return {
            "code": code.decode('utf-8')
        }
