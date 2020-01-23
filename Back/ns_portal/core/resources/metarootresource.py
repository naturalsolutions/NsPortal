from ns_portal.core.resources.restviews import (
    IRESTview
)
from zope.interface import implementer
# from webargs.pyramidparser import parser
from webargs.pyramidparser import PyramidParser


class Parser(PyramidParser):
    DEFAULT_VALIDATION_STATUS = 400


parser = Parser()  # global ref :( maybe not good
use_args = parser.use_args
use_kwargs = parser.use_kwargs


class CustomErrorParsingArgs(Exception):

    def __init__(self, value):
        print("error")
        self.value = value

    def __str__(self):
        return repr(self.value)


# @parser.error_handler
# def handle_error(error, req, schema, status_code, headers):
#     print("stop")
#     raise CustomErrorParsingArgs(error.messages)


@implementer(IRESTview)
class MetaRootResource (dict):
    __name__ = ''
    __parent__ = None
    __ROUTES__ = {}
    __specialKey__ = None
    __CORS__ = {
        'Access-Control-Allow-Origin': [
            'http://api.com'
            ],
        'Access-Control-Allow-Methods': [
            'GET',
            'HEAD',
            'POST',
            'DELETE',
            'OPTIONS',
            'TRACE',
            'PATCH',
            'PUT'
        ],
        'Access-Control-Allow-Headers': [
            'Authorization',
            'Content-Type'
        ],
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '86400'
    }

    def __init__(self, name, parent, request):
        self.__name__ = name
        self.__parent__ = parent
        # DON'T CHANGE THIS :)
        # webargs expect 'request' key in object for parsing
        # for now i don't know another or workaround
        self.request = request

    def __acl__(self):
        return []

    def __parser__(self, args={}):
        return parser.parse(args, req=self.request, location='querystring')

    @property
    def __specialKey__(self):
        return None

    @property
    def __routes__(self):
        return self.__ROUTES__

    def __getitem__(self, name):
        '''
        get item
        '''
        toRet = None

        if isinstance(self, MetaCollectionRessource):
            '''
            If the current node is a Collection
            the next node should be an instance of this collection
            by default REST say collection/{id}
            in most cases {id} = int
            so we have to check if the name is an int first
            but keep in min that Traversal use __getitem__
            and we can't populate all items with id
            so we need a special key {int} in our __routes__ dict

            TODO __specialKey__ should be declare is type
            and we check if name is same type
            '''
            try:
                int(name)
                toRet = self.__routes__.get(self.__specialKey__, None)
            except ValueError:
                raise KeyError((
                    f'the key for item should be and int: '
                    f'{self.__name__}'
                ))
        else:
            nextNode = name.lower()
            if nextNode != self.__specialKey__:
                toRet = self.__routes__.get(nextNode, None)

        if toRet is None:
            raise KeyError(f'__getitem__ for Ressource: {self.__name__}')
        else:
            return toRet(name=nextNode, parent=self, request=self.request)

    def GET(self):
        raise NotImplementedError(f'GET for Ressource: {self.__name__}')

    def HEAD(self):
        raise NotImplementedError(f'HEAD for Ressource: {self.__name__}')

    def POST(self):
        raise NotImplementedError(f'POST for Ressource: {self.__name__}')

    def DELETE(self):
        raise NotImplementedError(f'DELETE for Ressource: {self.__name__}')

    def OPTIONS(self):
        self.checkAndApplyCORS()
        return self.request.response
        # raise NotImplementedError(f'OPTIONS for Ressource: {self.__name__}')

    def TRACE(self):
        raise NotImplementedError(f'TRACE for Ressource: {self.__name__}')

    def PATCH(self):
        raise NotImplementedError(f'PATCH for Ressource: {self.__name__}')

    def PUT(self):
        raise NotImplementedError(f'PUT for Ressource: {self.__name__}')

    def checkHeadersRequestOrigin(self):
        '''
        request.headers['Origin'] is set by User-Agent browser
        we check if origin exist
        and if he is in the access control list
        if in the control list we will returned
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        not the entire access control list
        '''
        headers = {}
        requestHeaderKey = 'Origin'
        reqOrigin = self.request.headers.get(requestHeaderKey, None)
        responseHeaderKey = 'Access-Control-Allow-Origin'
        originsAllowed = self.__CORS__.get(responseHeaderKey)

        if reqOrigin is None:
            headers = False
        else:
            if (
                reqOrigin in originsAllowed
                or
                '*' in originsAllowed
            ):
                headers[responseHeaderKey] = reqOrigin
        return headers

    def checkHeadersRequestMethod(self):
        headers = {}
        requestHeaderKey = 'Access-Control-Request-Method'
        reqMethod = self.request.headers.get(requestHeaderKey, None)
        responseHeaderKey = 'Access-Control-Allow-Methods'
        methodsAllowed = self.__CORS__.get(responseHeaderKey)
        methodsStr = ','.join(methodsAllowed)

        if reqMethod is None:
            headers = False
        else:
            if reqMethod in methodsAllowed:
                headers[responseHeaderKey] = methodsStr
        return headers

    def checkHeadersRequestHeaders(self):
        headers = {}
        requestHeaderKey = 'Access-Control-Request-Headers'
        reqHeadersStr = self.request.headers.get(requestHeaderKey, None)
        if reqHeadersStr is not None:
            reqHeadersList = reqHeadersStr.split(',')
        responseHeadersKey = 'Access-Control-Allow-Headers'
        headersAllowed = self.__CORS__.get(responseHeadersKey)
        headersStr = ','.join(headersAllowed)

        if reqHeadersStr is None:
            headers[responseHeadersKey] = ''
        else:
            for reqHeader in reqHeadersList:
                if reqHeader not in headersAllowed:
                    headers = False
                    print(f'{reqHeader} is not allowed')
                    break
            if headers == {}:
                headers[responseHeadersKey] = headersStr

        return headers

    def checkHeadersRequestCredentials(self):
        headers = {}
        requestHeaderKey = 'Access-Control-Allow-Credentials'
        headers[requestHeaderKey] = self.__CORS__.get(requestHeaderKey)
        return headers

    def addHeadersMaxAge(self):
        headers = {}
        requestHeaderKey = 'Access-Control-Max-Age'
        headers[requestHeaderKey] = self.__CORS__.get('Access-Control-Max-Age')
        return headers

    def addHeadersForCORS(self, headers=None):
        self.request.response.headers.update(headers)

    def checkAndApplyCORS(self):
        orderedStepForCORS = [
            self.checkHeadersRequestOrigin,
            self.checkHeadersRequestMethod,
            self.checkHeadersRequestHeaders,
            self.checkHeadersRequestCredentials,
            self.addHeadersMaxAge
        ]
        stepHeaders = {}
        for method in orderedStepForCORS:
            stepHeaders = method()
            if stepHeaders is False:
                return self.request.response
            else:
                self.addHeadersForCORS(headers=stepHeaders)


class MetaEmptyRessource(MetaRootResource):
    pass


class MetaCollectionRessource(MetaRootResource):
    pass
