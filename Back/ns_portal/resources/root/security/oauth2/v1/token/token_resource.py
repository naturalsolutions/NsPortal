from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    EXCLUDE,
    ValidationError,
    pre_load,
    post_load
)
from ns_portal.database import (
    Main_Db_Base
)
from ns_portal.database.main_db import (
    TApplications,
    TUsers
)
from sqlalchemy import (
    select,
    and_
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound
)
from pyramid.security import (
    Allow,
    Everyone,
    _get_authentication_policy,
    remember
)
from pyramid.httpexceptions import (
    HTTPFound
)
from ns_portal.utils import (
    getToken
)


class tokenSchema(Schema):
    grant_type = fields.String(
        required=True
    )
    client_id = fields.String()
    client_secret = fields.String()
    code = fields.String()
    code_verifier = fields.String()
    password = fields.String()
    redirect_uri = fields.String()
    scope = fields.String()
    username = fields.String()

    # will exclude any key in request
    # not defined in schema
    class Meta:
        unknown = EXCLUDE

    @pre_load
    def validate_token(self, data, **kwargs):
        grantType, requiredList = self.checkGrantTypeAndGetOthersRequired(data)
        self.checkRequired(data, requiredList, grantType)
        self.validate_client_id(data)

        return data

    def checkRequired(self, data, requiredList, grantType):
        errors = {}
        for item in requiredList:
            if item not in data:
                errors[item] = (
                    f'is required in query string'
                    f' when grant_type is {grantType}'
                )

        if errors:
            raise ValidationError(errors)

    def checkGrantTypeAndGetOthersRequired(self, data):
        conf = {
                'authorization_code': [
                    'client_id',
                    'redirect_uri',
                    'code'
                    ],
                'client_credentials': [
                    'client_id',
                    'client_secret',
                    # 'scope'
                    ],
                'password': [
                    'client_id',
                    # 'client_secret',
                    'username',
                    'password'
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

    def doAuthorization_Code(self, data):

        print("ok on validate_grantType")
        print(f'et data : {data}')
        return True

    def validate_client_id(self, data):
        client_id = data.get('client_id')
        query = self.context['session'].query(TApplications)
        query = query.filter(
            TApplications.TApp_Name == client_id
            )
        try:
            res = query.one_or_none()
        except MultipleResultsFound:
            raise ValidationError({
                "client_id": (
                    f'not unique in db'
                    f' please report it to an admin'
                    )
                })
        if res:
            return data
        else:
            raise ValidationError({
                "client_id": (
                    f'not valid'
                    )
                })

    # we will add userId key in tokenSchema
    # will need it for token generation
    # optimisation for fetching credentials one time only
    @post_load
    def validateUserCredentials(self, data, **kwargs):
        query = self.context['session'].query(
            TUsers.TUse_PK_ID,
            TUsers.TUse_Language
            )
        query = query.filter(
            and_(
                TUsers.TUse_Login == data.get('username'),
                TUsers.TUse_Password == data.get('password')
                )
            )
        try:
            res = query.one_or_none()
        except MultipleResultsFound:
            raise ValidationError({
                "error": (
                    f'your username and password are'
                    f' not unique in db'
                    f' please report it to an admin'
                    )
                })
        if res:
            # this key is added after validation
            data['userId'] = res.TUse_PK_ID
            data['userLanguage'] = res.TUse_Language
            return data
        else:
            raise ValidationError({
                "error": (
                    f'your username and/or password'
                    f' are wrongs'
                    )
                })

    def doPassword(self, data):
        print("on do password")
        return True


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
            args=tokenSchema(
                context={
                    "session": self.request.dbsession
                }
            ),
            location='form'
        )
        # CRITICAL START
        # this method will return the object that handle
        # policy in pyramid app
        # the policy object store keys from conf for generate token
        policy = _get_authentication_policy(self.request)
        # CRITICAL END

        payload = self.buildPayload(params=reqParams, policy=policy)
        token = getToken(
            payload=payload,
            secret=getattr(policy, 'secretToken'),
            algorithm=getattr(policy, 'algorithm')
        )

        if reqParams.get('grant_type') == 'code':
            print("todo with other secret")

        if reqParams.get('grant_type') == 'password':
            remember(self.request, token)
            return HTTPFound(
                location='/',
                headers=self.request.response.headers
                )
