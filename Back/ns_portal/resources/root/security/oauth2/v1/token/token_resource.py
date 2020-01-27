from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    ValidationError,
    validates_schema,
    pre_load
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

    # @property
    # def session(self):
    #     print("toto")
    #     return "12"

    # @pre_load
    # def validate_token(self, data, **kwargs):
    #     step1_data = self.validate_grantType(data)

    @validates_schema
    def validate_token(self, data, **kwargs):
        errors = {}
        conf = {
            'grant_type': {
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
        }
        grantType = data['grant_type']
        grantTypeToTest = conf.get('grant_type').get(data['grant_type'])
        for item in grantTypeToTest:
            if item not in data:
                errors[item] = (
                    f'is required in query string'
                    f' when grant_type is {grantType}'
                )

        if errors:
            raise ValidationError(errors)


class TokenResource(MetaEndPointResource):

    def GET(self):
        requiredArgs = self.__parser__(
            args=tokenSchema(
                context={
                    "session": self.request.dbsession
                }
            )
        )
        print(requiredArgs)
        return "ok"
