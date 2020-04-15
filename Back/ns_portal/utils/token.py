import jwt
import datetime
from ns_portal.database.main_db import (
    TInstance,
    TApplications,
    TAutorisations,
    TUsers,
    TRoles,
    TSite
)
from ns_portal.utils.utils import (
    my_get_authentication_policy
)

# we follow the RFC7519
# look at https://tools.ietf.org/html/rfc7519#section-4.1
# for all definitions
_seconde = 1
_minuteInSec = 60 * _seconde
_hoursInSec = 60 * _minuteInSec

_cookieTokenExpInSec = 24 * _hoursInSec
_codeTokenExpInSec = 5
_accessTokenExpInSec = 5 * _minuteInSec
_refreshTokenExpInSec = 24 * _hoursInSec


def myEncode(payload, secret, algorithm):
    return jwt.encode(payload, secret, algorithm=algorithm)


def myDecode(token, secret):
    payloadValided = False
    try:
        payloadValided = jwt.decode(
            token,
            secret,
            algorithms=['HS256', 'HS512'],
            verify=False
            )
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError(
            'You take too much time for getting your token.',
            'You need to login again'
            )
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError(
            'Exception when decode()'
            )
    except jwt.DecodeError:
        raise jwt.DecodeError(
            'We canno\'t decode your token'
            )
    except jwt.InvalidSignatureError:
        raise jwt.InvalidSignatureError(
            'Your token’s signature doesn’t match'
            ' the one provided as part of the token'
        )
    return payloadValided


def getSecretAndAlgorithFromPolicy(request, tokenKey, algoKey):
    policy = my_get_authentication_policy(request)
    secret = getattr(policy, tokenKey)
    algorithm = getattr(policy, algoKey)

    return (secret, algorithm)


def getCookieToken(idUser, request):
    secret, algorithm = getSecretAndAlgorithFromPolicy(
        request=request,
        tokenKey='cookieTokenSecret',
        algoKey='cookieTokenAlgorithm'
        )

    payload = buildPayload(
        idUser=idUser,
        request=request,
        timeAddForExp=_cookieTokenExpInSec
        )

    return myEncode(payload, secret, algorithm)


def getCodeToken(idUser, request):
    secret, algorithm = getSecretAndAlgorithFromPolicy(
        request=request,
        tokenKey='codeTokenSecret',
        algoKey='codeTokenAlgorithm'
        )

    now = datetime.datetime.now()
    nowInTimeStampSeconds = int(now.timestamp())

    payload = {
        'sub': idUser,
        'exp': nowInTimeStampSeconds + _codeTokenExpInSec
    }

    return myEncode(payload, secret, algorithm=algorithm)


def buildPayload(idUser, request, timeAddForExp):
    policy = my_get_authentication_policy(request)
    tsiteName = getattr(policy, 'TSit_Name')

    colsToRet = [
        TInstance.TIns_PK_ID,
        TInstance.TIns_Label,
        TInstance.TIns_ApplicationPath,
        TInstance.TIns_Theme,
        TInstance.TIns_Database,
        TInstance.TIns_Order,
        TInstance.TIns_ReadOnly,
        TApplications.TApp_ClientID,
        TApplications.TApp_Description,
        TRoles.TRol_Label,
        TUsers.TUse_PK_ID,
        TUsers.TUse_Login,
        TUsers.TUse_Language,
        TSite.TSit_Name,
        TSite.TSit_Project,
        TSite.TSit_ImagePathMainLogo,
        TSite.TSit_ImagePathMainMenu,
        TAutorisations.TUse_Observer
    ]

    VAllUsersApplications = request.dbsession.query(TInstance)
    VAllUsersApplications = VAllUsersApplications.join(TApplications)
    VAllUsersApplications = VAllUsersApplications.join(
        TAutorisations,
        TInstance.TIns_PK_ID == TAutorisations.TAut_FK_TInsID
        )
    VAllUsersApplications = VAllUsersApplications.join(TRoles)
    VAllUsersApplications = VAllUsersApplications.join(TUsers)
    VAllUsersApplications = VAllUsersApplications.join(
        TSite,
        TInstance.TIns_FK_TSitID == TSite.TSit_PK_ID
        )

    VAllUsersApplications = VAllUsersApplications.with_entities(*colsToRet)

    VAllUsersApplications = VAllUsersApplications.filter(
            (TSite.TSit_Name == tsiteName),
            (TUsers.TUse_PK_ID == idUser),
            (TRoles.TRol_Label != 'Interdit')
        )
    VAllUsersApplications = VAllUsersApplications.order_by(
        TInstance.TIns_Order
        )

    result = VAllUsersApplications.all()

    now = datetime.datetime.now()
    nowInTimeStampSeconds = int(now.timestamp())

    payload = {
        "iss": 'NSPortal',
        "sub": str(result[0].TUse_PK_ID),
        "username": result[0].TUse_Login,
        "userlanguage": result[0].TUse_Language,
        'exp': nowInTimeStampSeconds + timeAddForExp,
        "roles": {
            row.TIns_Label: row.TRol_Label for row in result
        }
    }

    return payload


def getAccessToken(idUser, request):
    secret, algorithm = getSecretAndAlgorithFromPolicy(
        request=request,
        tokenKey='accessTokenSecret',
        algoKey='accessTokenAlgorithm'
        )

    payload = buildPayload(
        idUser=idUser,
        request=request,
        timeAddForExp=_accessTokenExpInSec
        )

    return myEncode(payload, secret, algorithm=algorithm)


def getRefreshToken(idUser, request):
    secret, algorithm = getSecretAndAlgorithFromPolicy(
        request=request,
        tokenKey='refreshTokenSecret',
        algoKey='refreshTokenAlgorithm'
        )

    now = datetime.datetime.now()
    nowInTimeStampSeconds = int(now.timestamp())

    payload = {
        'sub': idUser,
        'exp': nowInTimeStampSeconds + _refreshTokenExpInSec
    }

    return myEncode(payload, secret, algorithm=algorithm)
