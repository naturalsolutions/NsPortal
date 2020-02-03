from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    EXCLUDE,
    ValidationError,
    pre_load
)
from ns_portal.database import (
    Main_Db_Base
)
from sqlalchemy import (
    select
)
from pyramid.security import (
    Allow,
    Everyone,
    _get_authentication_policy
)
from ns_portal.utils import (
    getToken,
    myDecode
)


class tokenSchema(Schema):
    grant_type = fields.String(
        required=True
    )
    code = fields.String()

    # will exclude any key in request
    # not defined in schema
    class Meta:
        unknown = EXCLUDE

    @pre_load
    def validate_token(self, data, **kwargs):
        grantType, requiredList = self.checkGrantTypeAndGetOthersRequired(data)
        self.checkRequired(data, requiredList, grantType)

        return data

    def checkRequired(self, data, requiredList, grantType):
        errors = {}
        for item in requiredList:
            if item not in data:
                errors[item] = (
                    f'is required in json'
                    f' when grant_type is {grantType}'
                )

        if errors:
            raise ValidationError(errors)

    def checkGrantTypeAndGetOthersRequired(self, data):
        conf = {
                'code': [
                    'code'
                    ]
        }
        grantTypeInData = data.get('grant_type', None)
        if grantTypeInData is None:
            raise ValidationError({"grant_type": "required"})
        if grantTypeInData in conf:
            return grantTypeInData, conf.get(grantTypeInData)
        else:
            raise ValidationError({
                "grant_type": (
                    f'should be authorization_code'
                    f' client_credentials password'
                    )
                })


class TokenResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Everyone, 'create')
        ]

    def buildPayload(self, params, policy):
        viewToQuery = Main_Db_Base.metadata.tables['VAllUsersApplications']
        query = select([
            viewToQuery
        ]).where((
            viewToQuery.c['TSit_Name'] == getattr(policy, 'TSit_Name'))
            &
            (viewToQuery.c['TUse_PK_ID'] == params.get('userId'))
            &
            (viewToQuery.c['TRol_Label'] != 'Interdit'))
        query = query.order_by(viewToQuery.c['TIns_Order'])
        result = self.request.dbsession.execute(query).fetchall()
        payload = {
            "iss": 'NSPortal',
            "sub": params.get('userId'),
            "username": params.get('username'),
            "userlanguage": params.get('userLanguage'),
            "roles": {
                row.TIns_Label: row.TRol_Label for row in result
            }
        }

        return payload

    def POST(self):
        reqParams = self.__parser__(
            args=tokenSchema(),
            location='json'
        )
        policy = _get_authentication_policy(self.request)
        secret = getattr(policy, 'secretToken')
        print(f"secret token: {secret} code {reqParams.get('code')}")

        payloadInCode = myDecode(
            token=reqParams.get('code'),
            secret=secret
            )


        print(" check code ")
        token = getToken(
            idUser=self.request.authenticated_userid.get('TUse_PK_ID'),
            request=self.request
        )

        if reqParams.get('grant_type') == 'code':
            return {
                'token': token
            }

        # if reqParams.get('grant_type') == 'password':
        #     remember(self.request, token)
        #     return HTTPFound(
        #         location='/',
        #         headers=self.request.response.headers
        #         )
