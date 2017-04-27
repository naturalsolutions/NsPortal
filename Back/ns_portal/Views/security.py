from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import remember, forget, NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from ..Models import DBSession, User
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.response import Response

import transaction

route_prefix = 'security/'

@view_config(
    route_name=route_prefix+'login',
    permission=NO_PERMISSION_REQUIRED)
def login(request):

    if request.method == "OPTIONS":
        response = Response()
        response.headers['Access-Control-Expose-Headers'] = (
            'Content-Type, Date, Content-Length, Authorization, X-Request-ID, X-Requested-With')
        response.headers['Access-Control-Allow-Origin'] = (
            request.headers['Origin'])
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Origin, Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'
        response.headers['Access-Control-Allow-Methods'] = ('POST,GET,DELETE,PUT,OPTIONS')
        response.headers['Content-Type'] = ('application/json')
        return response


    user_id = request.POST.get('userId', '')
    pwd = request.POST.get('password', '')
    user = DBSession.query(User).filter(User.id==user_id).one()


    if user is not None and user.check_password(pwd):
        claims = {
            "iss": user_id,
            "username": user.Login,
            "userlanguage": user.Language
        }
        jwt = make_jwt(request, claims)
        response = Response(body='login success', content_type='text/plain')
        remember(response, jwt)
        transaction.commit()
        return response
    else:
        transaction.commit()
        return HTTPUnauthorized()

def make_jwt(request, claims):
    policy = request.registry.queryUtility(IAuthenticationPolicy)
    return policy.encode_jwt(request, claims)

@view_config(
    route_name=route_prefix+'logout',
    permission=NO_PERMISSION_REQUIRED,)
def logout(request):
    forget(request)
    return request.response

@view_config(route_name=route_prefix+'has_access')
def has_access(request):
    transaction.commit()
    return request.response
