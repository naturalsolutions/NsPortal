from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_renderer('json', JSON(indent=4))

    return config.make_wsgi_app()
