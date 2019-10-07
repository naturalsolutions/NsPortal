"""
Created on Mon Aug 25 13:00:16 2014

@author: Natural Solutions (Thomas)
"""

from ..Models import DBSession , User
import transaction 
from pyramid.httpexceptions import HTTPUnauthorized,HTTPForbidden
from pyramid_jwtauth import * 
from pyramid.security import (
    ALL_PERMISSIONS,
    DENY_ALL,
    Allow,
    Authenticated,
)

# Root class security #
class SecurityRoot(object):
    __acl__ = [
        (Allow, Authenticated, 'read'),
        (Allow, 'user', 'edit'),
        (Allow, 'admin', ALL_PERMISSIONS),
        DENY_ALL
    ]
    
    def __init__(self, request):
        self.request = request

# Useful fucntions #
def role_loader(user_id, request):
    result = DBSession.query(User.Role).filter(User.id==user_id).one()
    transaction.commit()
    return result

class myJWTAuthenticationPolicy(JWTAuthenticationPolicy):


    def get_userID(self, request):
        try :
            token = request.cookies.get("ecoReleve-Core")
            claims = self.decode_jwt(request, token)
            userid = claims['iss']
            return userid
        except: 
            return
    def get_userInfo(self, request):
        try :
            token = request.cookies.get("ecoReleve-Core")
            claims = self.decode_jwt(request, token, verify=True)
            return claims, True
        except: 
            try:
                token = request.cookies.get("ecoReleve-Core")
                claims = self.decode_jwt(request, token, verify=False)
                return claims,False
            except:
                return None, False

    def user_info(self, request):
        claim,verify_okay = self.get_userInfo(request)
        if claim is None:
            return None
        return claim

    def authenticated_userid(self, request):
        userid = self.get_userID(request)
        claim = self.user_info(request)

        if userid is None:
            return None
        return claim

    def unauthenticated_userid(self, request):
        userid = self.get_userID(request)
        return userid

    def remember(self, response, principal, **kw):
        if kw.get('domain') == '' :
            response.set_cookie('ecoReleve-Core', principal, max_age = 100000)
        else :
            response.set_cookie('ecoReleve-Core', principal, max_age = 100000, domain = kw.get('domain'))



    def forget(self, request):
        request.response.delete_cookie('ecoReleve-Core')

    def _get_credentials(self, request):
        return self.get_userID(request)

    def _check_signature(self, request):
        if request.environ.get('jwtauth.signature_is_valid', False):
            return True

    def challenge(self, request, content="Unauthorized"):
        if self.authenticated_userid(request):
            return HTTPUnauthorized(content, headers=self.forget(request))

        return HTTPForbidden(content, headers=self.forget(request))

