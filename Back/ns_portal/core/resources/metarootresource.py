from ns_portal.core.resources.restviews import (
    IRESTview
)
from zope.interface import implementer


@implementer(IRESTview)
class MetaRootResource (dict):
    __name__ = ''
    __parent__ = None
    __ROUTES__ = {}
    __specialKey__ = None

    def __init__(self, name, parent, request):
        self.__name__ = name
        self.__parent__ = parent
        # DON'T CHANGE THIS :)
        # webargs expect 'request' key in object for parsing
        # for now i don't know another or workaround
        self.request = request

    def __acl__(self):
        return []

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
        raise NotImplementedError(f'OPTIONS for Ressource: {self.__name__}')

    def TRACE(self):
        raise NotImplementedError(f'TRACE for Ressource: {self.__name__}')

    def PATCH(self):
        raise NotImplementedError(f'PATCH for Ressource: {self.__name__}')

    def PUT(self):
        raise NotImplementedError(f'PUT for Ressource: {self.__name__}')


class MetaEmptyRessource(MetaRootResource):
    pass


class MetaCollectionRessource(MetaRootResource):
    pass
