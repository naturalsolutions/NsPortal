from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_renderer('json', JSON(indent=4))
        config.include('ns_portal.routes')
        config.include('ns_portal.core.resources')
        config.include('ns_portal.resources')

    return config.make_wsgi_app()
