from pyramid.view import (
    view_config,
    view_defaults
)
from zope.interface import (
    Interface
)


class IRESTview(Interface):
    pass


@view_defaults(context=IRESTview)
class RESTview(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config(request_method='GET', renderer='json', permission='read')
    def GET(self):
        return self.context.GET()

    @view_config(request_method='HEAD', renderer='json', permission='read')
    def HEAD(self):
        return self.context.HEAD()

    @view_config(request_method='POST', renderer='json', permission='create')
    def POST(self):
        return self.context.POST()

    @view_config(request_method='DELETE', renderer='json', permission='delete')
    def DELETE(self):
        return self.context.DELETE()

    @view_config(request_method='OPTIONS', renderer='json', permission='read')
    def OPTIONS(self):
        return self.context.OPTIONS()

    @view_config(request_method='TRACE', renderer='json', permission='read')
    def TRACE(self):
        return self.context.TRACE()

    @view_config(request_method='PATCH', renderer='json', permission='update')
    def PATCH(self):
        return self.context.PATCH()

    @view_config(request_method='PUT', renderer='json', permission='update')
    def PUT(self):
        return self.context.PUT()
