from ns_portal.core.resources import (
    MetaRootResource,
    MetaEmptyRessource
)
from .security_views import (
    ISECURITYview
)
from zope.interface import implementer
from webargs import fields,validate
# from webargs.pyramidparser import use_args, parser



@implementer(ISECURITYview)
class VersionResource(MetaEmptyRessource):

    queryString = {
        'client_id':        fields.String(
            required=True,
            location='querystring'
            ),
        'response_type':    fields.String(
            required=True,
            location='querystring'
            ),
        'state':            fields.String(
            required=True,
            location='querystring'
            ),
        'redirect_uri':     fields.String(
            required=True,
            location='querystring'
            )
    }
    tokenArgs = {
        'grant_type': fields.String(
            required=True,
            validate=validate.Equal('client_credentials'),
            location='querystring'
            ),
        'client_id': fields.String(
            required=True,
            location='querystring'
            ),
        'client_secret': fields.String(
            required=True,
            location='querystring'
            )
    }

    def authorize(self):
        test = self.__parser__(args=self.queryString)
        print(test)
        return 'ok authorize'

    def logout(self):
        return 'ok logout'

    def token(self):
        requiredArgs = self.__parser__(args=self.tokenArgs)
        return "ok on te log"


class OAuth2Resource(MetaEmptyRessource):
    __ROUTES__ = {
        'v1': VersionResource
    }


class SecurityResource(MetaRootResource):

    __ROUTES__ = {
        'oauth2': OAuth2Resource
    }
