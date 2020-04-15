from pyramid.security import (
    _get_authentication_policy
)


def my_get_authentication_policy(request):
    # CRITICAL
    # _get_authentication_policy(request)
    # this method will return the instanciate singleton object that handle
    # policy in pyramid app
    # the policy object store keys from conf for generate token
    return _get_authentication_policy(request)
