corsConfig = {
    "domainewhitelist": [],
    "headersallow": []
}

__all__ = [
    "corsConfig"
]


def checkConfigForCORS(myConfig):
    if 'CORS.DOMAINWHITELIST' not in myConfig:
        raise KeyError('CORS.DOMAINWHITELIST key should be present in .ini')

    domaineWhitelist = myConfig.get('CORS.DOMAINWHITELIST', None)
    if domaineWhitelist is None or domaineWhitelist == '':
        raise ValueError(
            'Expected string for CORS.DOMAINWHITELIST ',
            'key got ({domaine}) '.format(domain=domaineWhitelist),
            'no values please define at leat one domain in *.ini'
            )

    if 'CORS.HEADERSALLOW' not in myConfig:
        raise KeyError('CORS.HEADERSALLOW key should be present in .ini')

    headersallow = myConfig.get('CORS.HEADERSALLOW', None)
    if headersallow is None or headersallow == '':
        raise ValueError(
            'Expected string for CORS.HEADERSALLOW ',
            'key got ({headers}) '.format(headers=headersallow),
            'no values please define at leat one header in *.ini'
            )


def getConfigForCORS(myConfig):
    checkConfigForCORS(myConfig=myConfig)
    domainInINI = myConfig.get('CORS.DOMAINWHITELIST')
    headersInINI = myConfig.get('CORS.HEADERSALLOW')
    corsConfig['domainewhitelist'] = domainInINI.split(',')
    corsConfig['headersallow'] = headersInINI.split(',')


def includeme(config):
    myConfig = config.get_settings()
    getConfigForCORS(myConfig=myConfig)

    config.include('.policy')
    config.include('.resources')
