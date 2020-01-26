from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    ValidationError,
    validates_schema
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
                    'scope'
                    ],
                'password': [
                    'client_id',
                    'client_secret',
                    'username',
                    'password'
                    ]
            }
        }
        typeGrant = data['grant_type']
        grantTypeToTest = conf.get('grant_type').get(data['grant_type'])
        for item in grantTypeToTest:
            if item not in data:
                errors[item] = f'is required when grant_type is {typeGrant}'

        if errors != {}:
            raise ValidationError(errors)


class TokenResource(MetaEndPointResource):

    def GET(self):
        requiredArgs = self.__parser__(args=tokenSchema())
        print(requiredArgs)
        return "ok"
