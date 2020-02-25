from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    EXCLUDE,
    ValidationError
)
from pyramid.security import (
    Allow,
    Authenticated,
    _get_authentication_policy
)
from ns_portal.database.main_db import (
    TInstance,
    TApplications,
    TAutorisations,
    TUsers,
    TRoles,
    TSite
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound
)
from ns_portal.utils import (
    getCodeToken
)
from pyramid.httpexceptions import (
    HTTPFound
)


class authorizeSchema(Schema):
    client_id = fields.String(required=True)
    redirect_uri = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class AuthorizeResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Authenticated, 'create')
    ]

    def validateSchema(self, data):
        client_id = data.get('client_id')
        redirect_uri = data.get('redirect_uri')

        policy = _get_authentication_policy(self.request)
        tsiteName = getattr(policy, 'TSit_Name')
        userId = self.request.authenticated_userid.get('TUse_PK_ID')

        colsToRet = [
            TInstance.TIns_PK_ID,
            TInstance.TIns_Label,
            TInstance.TIns_ApplicationPath,
            TInstance.TIns_Theme,
            TInstance.TIns_Database,
            TInstance.TIns_Order,
            TInstance.TIns_ReadOnly,
            TApplications.TApp_ClientID,
            TApplications.TApp_Description,
            TRoles.TRol_Label,
            TUsers.TUse_PK_ID,
            TSite.TSit_Name,
            TSite.TSit_Project,
            TSite.TSit_ImagePathMainLogo,
            TSite.TSit_ImagePathMainMenu,
            TAutorisations.TUse_Observer
        ]

        VAllUsersApplications = self.request.dbsession.query(TInstance)
        VAllUsersApplications = VAllUsersApplications.join(TApplications)
        VAllUsersApplications = VAllUsersApplications.join(
            TAutorisations,
            TInstance.TIns_PK_ID == TAutorisations.TAut_FK_TInsID
            )
        VAllUsersApplications = VAllUsersApplications.join(TRoles)
        VAllUsersApplications = VAllUsersApplications.join(TUsers)
        VAllUsersApplications = VAllUsersApplications.join(
            TSite,
            TInstance.TIns_FK_TSitID == TSite.TSit_PK_ID
            )

        VAllUsersApplications = VAllUsersApplications.with_entities(*colsToRet)

        VAllUsersApplications = VAllUsersApplications.filter(
                (TSite.TSit_Name == tsiteName),
                (TUsers.TUse_PK_ID == userId),
                (TRoles.TRol_Label != 'Interdit'),
                (TApplications.TApp_ClientID == client_id),
                (TInstance.TIns_ApplicationPath == redirect_uri)
            )
        VAllUsersApplications = VAllUsersApplications.order_by(
            TInstance.TIns_Order
            )
        try:
            res = VAllUsersApplications.one_or_none()
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

        code = getCodeToken(
            idUser=self.request.authenticated_userid.get('TUse_PK_ID'),
            request=self.request
        )

        self.request.response.json_body = {
            "code": code.decode('utf-8')
        }
        return self.request.response
