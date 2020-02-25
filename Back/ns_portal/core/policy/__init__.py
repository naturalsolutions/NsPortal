from .authentificationPolicy import (
        MyAuthenticationPolicy,
        myAuthorizationPolicy
)

_defaultCookieName = 'NSPORTAL'
_defaultAlgorithm = 'HS512'


def includeme(config):
    authorizationPolicy = myAuthorizationPolicy()
    config.set_authorization_policy(authorizationPolicy)

    customSettings = meaningConfig(config)

    authentificationPolicy = MyAuthenticationPolicy(**customSettings)
    config.set_authentication_policy(authentificationPolicy)

    # from now all view added to project will have 'read' permission by default
    # but BE CAREFUL and read the doc
    # https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#setting-a-default-permission
    # short way :
    # use NO_PERMISSION_REQUIRED for overwrite this default permission
    config.set_default_permission('read')


def meaningConfig(config):
    '''
    pick params with need in *.ini file
    '''
    settings = config.get_settings()
    if settings.get('RENECO.SECURITE.TINS_LABEL') is None:
        '''
        this key is used to check your cookie claims
        if you are on SERVER B with an instance of ecoReleve
        You must have an Tins_Label to identify the app
        Tips:
        The portal give you a domain cookie
        with all instance of all app
        on the server and your user role encoded in the payload
        like this ['role'] : {
        Tins_label : role
        }
        (example : erd PROD, erd DEV )
        '''
        raise Exception(
            f'You mus\'t have this key RENECO.SECURITE.TINS_LABEL'
            f'defined in your *.ini file'
        )

    if settings.get('RENECO.SECURITE.TSIT_NAME') is None:
        '''
        '''
        raise Exception(
            f'You mus\'t have this key RENECO.SECURITE.TSIT_NAME'
            f'defined in your *.ini file'
        )

    return {
            "cookieTokenSecret": settings.get(
                'JWTSECURITY.COOKIETOKENMASTER_SECRET',
                None
                ),
            "cookieTokenAlgorithm": settings.get(
                'JWTSECURITY.COOKIETOKENALGORITHM',
                None
                ),
            "accessTokenSecret": settings.get(
                'JWTSECURITY.ACCESSTOKENMASTER_SECRET',
                None
                ),
            "accessTokenAlgorithm": settings.get(
                'JWTSECURITY.ACCESSTOKENALGORITHM',
                None
                ),
            "codeTokenSecret": settings.get(
                'JWTSECURITY.CODETOKENMASTER_SECRET',
                None
                ),
            "codeTokenAlgorithm": settings.get(
                'JWTSECURITY.CODETOKENALGORITHM',
                None
                ),
            "refreshTokenSecret": settings.get(
                'JWTSECURITY.REFRESHTOKENMASTER_SECRET',
                None
                ),
            "refreshTokenAlgorithm": settings.get(
                'JWTSECURITY.REFRESHTOKENALGORITHM',
                None
                ),
            "cookie_name": settings.get(
                'JWTSECURITY.COOKIENAME',
                None
                ),
            "TIns_Label": settings.get(
                'RENECO.SECURITE.TINS_LABEL'
                ),
            "TSit_Name": settings.get(
                'RENECO.SECURITE.TSIT_NAME'
                )
    }
