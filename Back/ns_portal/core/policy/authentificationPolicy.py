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
from ns_portal.database.main_db import (
    TUsers,
    TUsersSchema
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound
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
        # algorithm=None,
        # secretToken=None,
        # secretCode=None,
        # secretRefreshToken=None,
        cookieTokenSecret=None,
        cookieTokenAlgorithm=None,
        accessTokenSecret=None,
        accessTokenAlgorithm=None,
        codeTokenSecret=None,
        codeTokenAlgorithm=None,
        refreshTokenSecret=None,
        refreshTokenAlgorithm=None,
        cookie_name=None,
        TIns_Label=None,
        TSit_Name=None
    ):

        self.cookie_name = cookie_name
        #   Welcome to the real world neo :D
        #   from    *.ini  key = ecorelevé
        #   parsed         key = ecoRelevÃ©
        #   encoded to latin1 and decoded in utf-8
        # you get back key = ecorelevé lol ? so fun...
        self.TIns_Label = TIns_Label.encode('latin1').decode('utf-8')
        self.TSit_Name = TSit_Name

        if cookieTokenSecret is None:
            raise ValueError('cookieTokenSecret should not be empty')
        else:
            self.cookieTokenSecret = bytes(
                cookieTokenSecret,
                encoding='utf-8'
                )
        if cookieTokenAlgorithm is None:
            raise ValueError('cookieTokenAlgorithm should not be empty')
        else:
            self.cookieTokenAlgorithm = cookieTokenAlgorithm

        if accessTokenSecret is None:
            raise ValueError('accessTokenSecret should not be empty')
        else:
            self.accessTokenSecret = bytes(
                accessTokenSecret,
                encoding='utf-8'
                )
        if accessTokenAlgorithm is None:
            raise ValueError('accessTokenAlgorithm should not be empty')
        else:
            self.accessTokenAlgorithm = accessTokenAlgorithm

        if codeTokenSecret is None:
            raise ValueError('codeTokenSecret should not be empty')
        else:
            self.codeTokenSecret = bytes(
                codeTokenSecret,
                encoding='utf-8'
                )
        if codeTokenAlgorithm is None:
            raise ValueError('codeTokenAlgorithm should not be empty')
        else:
            self.codeTokenAlgorithm = codeTokenAlgorithm

        if refreshTokenSecret is None:
            raise ValueError('refreshTokenSecret should not be empty')
        else:
            self.refreshTokenSecret = bytes(
                refreshTokenSecret,
                encoding='utf-8'
                )
        if refreshTokenAlgorithm is None:
            raise ValueError('refreshTokenAlgorithm should not be empty')
        else:
            self.refreshTokenAlgorithm = refreshTokenAlgorithm

        self.callback = self.getClaims

    def getClaims(self, allClaims, request):
        return allClaims

    def effective_principals(self, request):
        principals = [Everyone]
        user = self.authenticated_userid(request)
        if user:
            principals += [Authenticated]

        return principals

    def checkUserInDb(self, request, claims):
        idUser = claims.get('sub')
        query = request.dbsession.query(
            TUsers.TUse_PK_ID,
            TUsers.TUse_LastName,
            TUsers.TUse_FirstName,
            TUsers.TUse_CreationDate,
            TUsers.TUse_Login,
            TUsers.TUse_Language,
            TUsers.TUse_ModificationDate,
            TUsers.TUse_HasAccess,
            TUsers.TUse_Photo,
            TUsers.TUse_PK_ID_OLD
            )
        query = query.filter(
                    TUsers.TUse_PK_ID == idUser
                )
        try:
            res = query.one_or_none()
            return TUsersSchema().dump(res) if res else None
        except MultipleResultsFound:
            raise MultipleResultsFound()

        return res

    def authenticated_userid(self, request):
        '''
        this function will check if datas (sub and role )
        in cookie's payload in request
        match datas in database when you do the request

        for later or specific case
        '''

        userCookieClaims = self.unauthenticated_userid(request)
        if userCookieClaims is not None:
            user = self.checkUserInDb(request, userCookieClaims)
            return user

        return None

    def unauthenticated_userid(self, request):
        userCookieClaims = None
        cookie = request.cookies.get(self.cookie_name)
        if cookie:
            userCookieClaims = self.extractClaimsFromCookie(cookie)

        return userCookieClaims

    def extractClaimsFromCookie(self, jwt):
        claims = None

        claims = myDecode(
            token=jwt,
            secret=self.cookieTokenSecret
            )
        return claims

    def remember(self, response, token):

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
        response.set_cookie(
            name=self.cookie_name,
            value=token,
            max_age=maxAge,
            path='/',
            domain=None,
            secure=False,
            httponly=False,
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
