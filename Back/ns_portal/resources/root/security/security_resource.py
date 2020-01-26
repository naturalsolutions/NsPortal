from ns_portal.core.resources import (
    MetaRootResource
)
from .oauth2 import (
    OAuth2Resource
)


class SecurityResource(MetaRootResource):

    __ROUTES__ = {
        'oauth2': OAuth2Resource
    }


# from .security_views import (
#     ISECURITYview
# )
# from zope.interface import implementer
# from webargs import fields,validate
# # from webargs.pyramidparser import use_args, parser
# from marshmallow import (
#     Schema,
#     fields,
#     ValidationError,
#     validates_schema
# )
# class tokenSchema(Schema):
#     grant_type = fields.String(
#         required=True
#     )
#     client_id = fields.String()
#     client_secret = fields.String()
#     code = fields.String()
#     code_verifier = fields.String()
#     password = fields.String()
#     redirect_uri = fields.String()
#     scope = fields.String()
#     username = fields.String()

#     @validates_schema
#     def validate_token(self, data, **kwargs):
#         errors = {}
#         conf = {
#             'grant_type' : {
#                 'authorization_code' : ['client_id', 'scope', 'redirect_uri', 'code', 'code_verifier'],
#                 'client_credentials' : ['client_id', 'client_secret', 'scope'],
#                 'password' : ['client_id', 'client_secret', 'username', 'password']
#             }
#         }
#         typeGrant = data['grant_type']
#         grantTypeToTest = conf.get('grant_type').get(data['grant_type'])
#         for item in grantTypeToTest:
#             if item not in data:
#                 errors[item] = f'is required when grant_type is {typeGrant}'

#         # if data['grant_type'] == 'authorization_code':
#         #     requiredFields = ['client_id', 'scope', 'redirect_uri', 'code', 'code_verifier']
#         #     for item in requiredFields:
#         #         if item not in data:
#         #             errors[item] = f'is required when grant_type is {data["grant_type"]}'
#         #             # raise ValidationError(f'{item} is required when grant_type is {data["grant_type"]}')
#         # if data['grant_type'] == 'client_credentials':
#         #     requiredFields = ['client_id', 'client_secret', 'scope']
#         #     for item in requiredFields:
#         #         if item not in data:
#         #             # raise ValidationError(f'{item} is required when grant_type is {data["grant_type"]}')
#         # if data['grant_type'] == 'password':
#         #     requiredFields = ['client_id', 'client_secret', 'username', 'password']
#         #     for item in requiredFields:
#         #         if item not in data:
#         #             # raise ValidationError(f'{item} is required when grant_type is {data["grant_type"]}')

#         if errors != {}:
#             raise ValidationError(errors)
#             # modifier required
#             print("on va etablir les regles a valider pour le grant-type: code")





# @implementer(ISECURITYview)
# class VersionResource(MetaEmptyRessource):

#     # queryString = {
#     #     'client_id':        fields.String(
#     #         required=True,
#     #         location='querystring'
#     #         ),
#     #     'response_type':    fields.String(
#     #         required=True,
#     #         location='querystring'
#     #         ),
#     #     'state':            fields.String(
#     #         required=True,
#     #         location='querystring'
#     #         ),
#     #     'redirect_uri':     fields.String(
#     #         required=True,
#     #         location='querystring'
#     #         )
#     # }
#     # tokenArgs = {
#     #     'grant_type': fields.String(
#     #         required=True,
#     #         validate=validate.OneOf(['client_credentials','password','authorization_code']),
#     #         location='querystring'
#     #         ),
#     #     'client_id': fields.String(
#     #         required=True,
#     #         location='querystring'
#     #         ),
#     #     'client_secret': fields.String(
#     #         required=True,
#     #         location='querystring'
#     #         ),
#     #     'code': fields.String(),
#     #     'code_verifier' : fields.String(),
#     #     'password': fields.String(),
#     #     'redirect_uri': fields.String(),
#     #     'scope': fields.String(),
#     #     'username': fields.String()
#     # }

#     def authorize(self):
#         # test = self.__parser__(args=self.queryString)
#         print(test)
#         return 'ok authorize'

#     def logout(self):
#         return 'ok logout'

#     def token(self):
#         requiredArgs = self.__parser__(args=tokenSchema())
#         return "ok on te log"

#     def login(self):
#         return 'yolo'
