import jwt
import datetime

# we follow the RFC7519
# look at https://tools.ietf.org/html/rfc7519#section-4.1
# for all definitions
_seconde = 1
_minute = 60 * _seconde

_nbMinBeforeExpired = 5

_deltaValidInSeconds = 60


def getOauth2CodeWithSecret(idUser, secret, algorithm):
    now = datetime.datetime.now()
    nowInTimeStampSeconds = int(now.timestamp())

    payload = {
        'iss': 'NSPortal',
        'sub': idUser,
        'exp': nowInTimeStampSeconds + _nbMinBeforeExpired * (_minute),
        'iat': nowInTimeStampSeconds
    }

    return myEncode(payload, secret, algorithm=algorithm)


def myEncode(payload, secret, algorithm):
    return jwt.encode(payload, secret, algorithm=algorithm)


def myDecode(code, secret, listAlgorithm):
    payloadValided = False
    try:
        payloadValided = jwt.decode(code, secret, algorithms=listAlgorithm)
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


def checkOauth2CodeAndGiveToken(code, secret, listAlgorithm):
    return myDecode(code, secret, listAlgorithm)


def getToken(payload, secret, algorithm):
    return myEncode(payload, secret, algorithm)
