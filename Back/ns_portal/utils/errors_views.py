from pyramid.view import (
    view_config,
    forbidden_view_config
)
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPNotImplemented,
    HTTPUnauthorized,
    HTTPForbidden
)
from ns_portal.core.resources.metarootresource import (
    CustomErrorParsingArgs,
    MyNotImplementedError
)
from marshmallow import (
    ValidationError
)


@view_config(context=ValidationError)
def validationError_marsh(exception, request):
    return Response(
        status=400,
        content_type='application/json',
        charset='utf-8',
        json_body=exception.messages
        )


@view_config(context=CustomErrorParsingArgs)
def failed_sqlalchemy(exception, request):
    """
    catch any CustomErrorParsingArgs raised
    """

    return Response(
        status=400,
        content_type='application/json',
        charset='utf-8',
        body=f'{exception}'
        )


@view_config(context=MyNotImplementedError)
def myNotImplementedView(exception, request):
    """
    catch any MyNotImplementedError raised
    """
    print(
        f'DEBUG HINT\n'
        f'API called with request\n'
        f'METHOD : {exception.method}\n'
        f'URL : {exception.path_url}\n'
        f'QUERY STRING: {exception.query_string}\n'
        f'this method is not yet implemented\n'
    )

    return HTTPNotImplemented(
        headers={
            "content_type": 'application/json',
            "charset": 'utf-8',
        },
        body=f'{exception}'
        )


@forbidden_view_config()
def forbidden(request):
    '''
    IF no cookie in the request
    or when effective_principals in cookie didn't match view permission
    HTTPForbidden() is raised

    forbidden_view_config is an hook that invoke the method when
    HTTPForbidden() is raised (when is RAISED! not whend returned)
    '''

    # case when no cookie
    # return 401
    if getattr(request, 'authenticated_userid') is None:
        return HTTPUnauthorized('No cookie')

    # effective_principals didn't match
    # return 403
    return HTTPForbidden()
