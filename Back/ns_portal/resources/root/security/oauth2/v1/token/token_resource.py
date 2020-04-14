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
from pyramid.httpexceptions import (
    HTTPBadRequest
)
from ns_portal.utils import (
    getAccessToken,
    getRefreshToken,
    myDecode
)
import datetime


class tokenSchema(Schema):
    grant_type = fields.String(
        required=True
    )
    code = fields.String()
    refresh_token = fields.String()

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
                    'is required in json ',
                    'when grant_type is {grantType}'.format(grantType=grantType)
                )

        if errors:
            raise ValidationError(errors)

    def checkGrantTypeAndGetOthersRequired(self, data):
        conf = {
                'code': [
                    'code'
                    ],
                'refresh_token': [
                    'refresh_token'
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
                    'should be code'
                    ' refresh_token'
                    )
                })


class TokenResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Everyone, 'create'),
        (Allow, Everyone, 'CORS')
        ]

    def POST(self):
        reqParams = self.__parser__(
            args=tokenSchema(),
            location='json'
        )
        policy = _get_authentication_policy(self.request)

        if reqParams.get('grant_type') == 'code':
            secret = getattr(policy, 'codeTokenSecret')
            payloadInCode = myDecode(
                token=reqParams.get('code'),
                secret=secret
                )
            now = datetime.datetime.now()
            dateExpCode = datetime.datetime.fromtimestamp(
                payloadInCode.get('exp')
                )
            if now < dateExpCode:
                accessToken = getAccessToken(
                    idUser=payloadInCode.get('sub'),
                    request=self.request
                )
                refreshToken = getRefreshToken(
                    idUser=payloadInCode.get('sub'),
                    request=self.request
                )

                self.request.response.json_body = {
                    'access_token': accessToken.decode('utf-8'),
                    'token_type': 'Bearer',
                    "expires_in": 300,
                    "refresh_token": refreshToken.decode('utf-8')
                    }
                return self.request.response
            else:
                return HTTPBadRequest("Code no more valid")
        elif reqParams.get('grant_type') == 'refresh_token':
            secret = getattr(policy, 'refreshTokenSecret')
            payloadInRefreshToken = myDecode(
                token=reqParams.get('refresh_token'),
                secret=secret
                )
            now = datetime.datetime.now()
            dateExpCode = datetime.datetime.fromtimestamp(
                payloadInRefreshToken.get('exp')
                )
            if now < dateExpCode:
                accessToken = getAccessToken(
                    idUser=payloadInRefreshToken.get('sub'),
                    request=self.request
                )

                self.request.response.json_body = {
                    'access_token': accessToken.decode('utf-8'),
                    'token_type': 'Bearer',
                    "expires_in": 300
                    }
                return self.request.response
            else:
                return "refresh token no more valid"
        else:
            return HTTPBadRequest('Code no more valid')
