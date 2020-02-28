from ns_portal.resources import root_factory


def includeme(config):
    '''
    every resources or actions in this API will start by this object
    be careful if you try to mix urlDispatch and traversal algorithm
    keep it in mind
    '''
    config.set_root_factory(root_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
