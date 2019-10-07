from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import remember, forget, NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from ..Models import DBSession, User, Base, dbConfig
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.response import Response

from sqlalchemy import select

import transaction

route_prefix = 'security/'

@view_config(
    route_name=route_prefix+'login',
    permission=NO_PERMISSION_REQUIRED,
    request_method='POST')
def login(request):
    user_id = request.POST.get('userId', '')
    pwd = request.POST.get('password', '')
    user = DBSession.query(User).filter(User.id==user_id).one()
    if user is not None and user.check_password(pwd):
        table = Base.metadata.tables['VAllUsersApplications']
        query = select([
            table
        ]).where((table.c['TSit_Name'] == dbConfig['siteName']) & (table.c['TUse_PK_ID'] == user_id) & (table.c['TRol_Label'] != 'Interdit')).order_by(table.c['TIns_Order'])
        result = DBSession.execute(query).fetchall()
        claims = {
            "iss": user_id,
            "sub": user_id,
            "username": user.Login,
            "userlanguage": user.Language,
            "roles" : {
                row.TIns_Label : row.TRol_Label for row in result
            }
        }
            
        jwt = make_jwt(request, claims)
        response = Response(body='login success', content_type='text/plain')
        
        try:
            domain = '.' + request.registry.settings['parent_domain']
        except:
            domain = ''

        remember(response, jwt, domain=domain)
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
