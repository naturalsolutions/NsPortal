from pyramid.view import (
    view_config,
    view_defaults
)
from pyramid.security import (
    NO_PERMISSION_REQUIRED
)
from zope.interface import (
    Interface
)


class ISECURITYview(Interface):
    pass


@view_defaults(context=ISECURITYview, renderer='json')
class SECURITYview(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config(
        request_method='POST',
        name="login",
        permission=NO_PERMISSION_REQUIRED
    )
    def login(self):
        return self.context.login()

    @view_config(
        request_method='GET',
        name="logout",
        permission=NO_PERMISSION_REQUIRED
    )
    def logout(self):
        return self.context.logout()

    @view_config(
        request_method='GET',
        name="authorize",
        permission=NO_PERMISSION_REQUIRED
    )
    def authorize(self):
        return self.context.authorize()

    @view_config(
        request_method='GET',
        name="token",
        permission=NO_PERMISSION_REQUIRED
    )
    def token(self):
        return self.context.token()
