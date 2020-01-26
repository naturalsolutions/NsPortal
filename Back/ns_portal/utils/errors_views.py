from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPNotImplemented
)
from ns_portal.core.resources.metarootresource import (
    CustomErrorParsingArgs,
    MyNotImplementedError
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
