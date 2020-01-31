from pyramid.config import Configurator
from pyramid.renderers import JSON
import base64


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        def bytes_adapter(obj, request):
            return base64.b64encode(obj).decode()
        json_renderer = JSON(indent=4)
        json_renderer.add_adapter(bytes, bytes_adapter)

        config.add_renderer('json', json_renderer)
        config.include('ns_portal.database')
        config.include('ns_portal.core.policy')
        config.include('ns_portal.core.resources')
        config.include('ns_portal.routes')
        config.include('ns_portal.utils')

    return config.make_wsgi_app()
