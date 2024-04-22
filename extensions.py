from meta_registry import MetaRegistry
from modules.wordpress.extensions import wordpress_registry
from modules.translate.extensions import translate_registry
from modules.get_robots.extensions import get_robots_registry
from modules.openpeoplesearch.extensions import openpeoplesearch_registry

registry = MetaRegistry()
registry.include_registry("wordpress", wordpress_registry)
registry.include_registry("get_robots", get_robots_registry)
registry.include_registry("translate", translate_registry)
registry.include_registry("openpeoplesearch", openpeoplesearch_registry)