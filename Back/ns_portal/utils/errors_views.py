from pyramid.view import view_config
from pyramid.response import Response
from ns_portal.core.resources.metarootresource import CustomErrorParsingArgs


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