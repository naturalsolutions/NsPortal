from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    # validates,
    ValidationError,
    # validates_schema,
    pre_load
)
from ns_portal.database.main_db import (
    TApplications,
    TUsers
)
from sqlalchemy import (
    and_
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound
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

    @pre_load
    def validate_token(self, data, **kwargs):
        stepVsGrantType = {
            'authorization_code': self.doAuthorization_Code,
            'client_credentials': [
                self.validate_client_id
                ],
            'password': [
                self.validate_client_id,
                self.validateUserCredentials
                ]
        }

        grantType, requiredList = self.checkGrantTypeAndGetOthersRequired(data)
        self.checkRequired(data, requiredList, grantType)
        algo = stepVsGrantType.get(grantType)
        for step in algo:
            step(data)

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
                    'scope',
                    'redirect_uri',
                    'code',
                    'code_verifier'
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
            return True
        else:
            raise ValidationError({
                "client_id": (
                    f'not valid'
                    )
                })

    def validateUserCredentials(self, data):
        query = self.context['session'].query(TUsers.TUse_PK_ID)
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
            return True
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

    def POST(self):
        requiredArgs = self.__parser__(
            args=tokenSchema(
                context={
                    "session": self.request.dbsession
                }
            ),
            location='form'
        )
        print(requiredArgs)
        print("validation is ok")
        print("generate token")
        return "ok"
