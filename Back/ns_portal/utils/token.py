import jwt
import datetime
from pyramid.security import (
    _get_authentication_policy
)

# we follow the RFC7519
# look at https://tools.ietf.org/html/rfc7519#section-4.1
# for all definitions
_seconde = 1
_minute = 60 * _seconde

_nbMinBeforeExpired = 5

_deltaValidInSeconds = 60


def getOauth2CodeWithSecret(idUser, client_id, request):

    policy = _get_authentication_policy(request)
    secret = getattr(policy, 'secretToken')
    algorithm = getattr(policy, 'algorithm')

    now = datetime.datetime.now()
    nowInTimeStampSeconds = int(now.timestamp())

    payload = {
        'sub': idUser,
        'exp': nowInTimeStampSeconds + _nbMinBeforeExpired * (_minute)
    }

    return myEncode(payload, secret, algorithm='HS256')


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
            f'You take too much time for getting your token.',
            f'You need to login again'
            )
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError(
            f'Exception when decode()'
            )
    except jwt.DecodeError:
        raise jwt.DecodeError(
            f'We canno\'t decode your token'
            )
    except jwt.InvalidSignatureError:
        raise jwt.InvalidSignatureError(
            f'Your token’s signature doesn’t match'
            f' the one provided as part of the token'
        )
    return payloadValided


def checkOauth2CodeAndGiveToken(code, secret):
    return myDecode(
        token=code,
        secret=secret
        )


def getToken(idUser, request):

    policy = _get_authentication_policy(request)
    secret = getattr(policy, 'secretToken')
    algorithm = getattr(policy, 'algorithm')

    now = datetime.datetime.now()
    nowInTimeStampSeconds = int(now.timestamp())

    payload = {
        'sub': idUser,
        'exp': nowInTimeStampSeconds + _nbMinBeforeExpired * (_minute)
    }


    return myEncode(payload, secret, algorithm)
