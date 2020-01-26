from ns_portal.resources.root import MyRoot


def root_factory(request):
    '''
    The first node of ou api
    '''
    return MyRoot(name='', parent=None, request=request)
