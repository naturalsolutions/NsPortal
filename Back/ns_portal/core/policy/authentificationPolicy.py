from zope.interface import (
    implementer
)
from pyramid.interfaces import (
    IAuthenticationPolicy
)
from pyramid.authentication import (
    CallbackAuthenticationPolicy
)
from pyramid.authorization import (
    ACLAuthorizationPolicy
)
from pyramid.security import (
    Everyone,
    Authenticated
)
from ns_portal.utils import (
    myDecode
)


@implementer(IAuthenticationPolicy)
class MyAuthenticationPolicy(CallbackAuthenticationPolicy):

    """
    A custom authentification policy
    This object will be create once

    Constructor Arguments

    ``header``
        A dict or a JSON string with the JWT Header data.

    """

    def __init__(
        self,
        algorithm=None,
        secretToken=None,
        secretCode=None,
        secretRefreshToken=None,
        cookie_name=None,
        TIns_Label=None,
        TSit_Name=None
    ):

        self.algorithm = algorithm
        self.cookie_name = cookie_name
        #   Welcome to the real world neo :D
        #   from    *.ini  key = ecorelevé
        #   parsed         key = ecoRelevÃ©
        #   encoded to latin1 and decoded in utf-8
        # you get back key = ecorelevé lol ? so fun...
        self.TIns_Label = TIns_Label.encode('latin1').decode('utf-8')
        self.TSit_Name = TSit_Name

        if secretToken is None:
            raise ValueError('secretToken should not be empty')
        else:
            self.secretToken = bytes(
                secretToken,
                encoding='utf-8'
                )

        if secretCode is None:
            raise ValueError('secretCode should not be empty')
        else:
            self.secretCode = bytes(
                secretCode,
                encoding='utf-8'
                )

        if secretRefreshToken is None:
            raise ValueError('secretRefreshToken should not be empty')
        else:
            self.secretRefreshToken = bytes(
                secretRefreshToken,
                encoding='utf-8'
                )

        self.callback = self.getClaims

    def getClaims(self, allClaims, request):
        return allClaims

    def effective_principals(self, request):
        principals = [Everyone]
        verifedClaims = self.authenticated_userid(request)
        if verifedClaims:
            principals += [Authenticated]
            # map new with old :(
            GROUPS = {
                'Super Utilisateur': 'group:superUser',
                'Utilisateur': 'group:user',
                'Administrateur': 'group:admin'
            }

            if 'roles' in verifedClaims:
                cookieRole = verifedClaims['roles'].get(self.TIns_Label, None)
                if cookieRole:
                    principals += [GROUPS.get(cookieRole, None)]

        return principals

    def authenticated_userid(self, request):
        '''
        this function will check if datas (sub and role )
        in cookie's payload in request
        match datas in database when you do the request

        for later or specific case
        '''

        verifedClaims = None
        userCookieClaims = self.unauthenticated_userid(request)
        if userCookieClaims is not None:
            effectiveClaimsOnRequestTime = self.getClaims(
                userCookieClaims,
                request
            )
            if effectiveClaimsOnRequestTime is None:
                return verifedClaims
            # DUMB TEST (we trust cookie payload )!!!! that's not really "verfiedClaims"
            # if you really want to "verify"" claims role in cookie match TRUE roles in database when request is invoked
            # you should make a request to database and implement your own check :) dunno if it's really possible with import scaffold for now and sqlachemy dbsession
            # if (
            #     userCookieClaims.get('roles').get(self.TIns_Label) ==
            #     effectiveClaimsOnRequestTime.get('roles').get(self.TIns_Label)
            # ):
            verifedClaims = effectiveClaimsOnRequestTime

        return verifedClaims

    def unauthenticated_userid(self, request):
        userCookieClaims = None
        cookie = request.cookies.get(self.cookie_name)
        if cookie:
            userCookieClaims = self.extractClaimsFromCookie(cookie)

        return userCookieClaims

    def extractClaimsFromCookie(self, jwt):
        claims = None

        claims = myDecode(jwt, self.secretToken, listAlgorithm=[self.algorithm])
        return claims

    def remember(self, request, token):

        '''
        call by login view
        given userid we gonna generate claims add in payload
        will generate cookie headers for response

        '''
        Sec = 1
        Mins = 60 * Sec
        Hours = 60 * Mins
        Days = 24 * Hours
        Weeks = 7 * Days

        maxAge = 1 * Days

        # secure=False
        # becareful if activated cookie will travel only on securized canal (HTTPS)

        # httponly=True
        # security manipulate cookie by javascript in client
        request.response.set_cookie(
            name=self.cookie_name,
            value=token,
            max_age=maxAge,
            path='/',
            domain=None,
            secure=False,
            httponly=True,
            comment=None,
            expires=None,
            overwrite=False,
            samesite=None
        )

    def forget(self, request):
        '''
        Delete a cookie from the client.  Note that ``path`` and ``domain``
        must match path and domain the cookie was originally set.

        Will sets the cookie to the empty string, and ``max_age=0`` so
        that it should expire immediately.
        '''
        request.response.delete_cookie(
            name=self.cookie_name,
            path='/',
            domain=None
        )


class myAuthorizationPolicy(ACLAuthorizationPolicy):
    def authenticated_userid(self, request):
        print("authenticated_userid policy")
        return []

    def effective_principals(self, request):
        print("effective_principals policy")
        return []
