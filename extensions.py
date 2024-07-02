from meta_registry import MetaRegistry
from modules.wordpress.extensions import wordpress_registry
from modules.translate.extensions import translate_registry
from modules.get_robots.extensions import get_robots_registry
from modules.openpeoplesearch.extensions import openpeoplesearch_registry
from modules.leakcheck.extensions import leakcheck_registry
from modules.Maigret.extensions import Maigret_registry
from modules.freecnam.extensions import freecnam_registry
from modules.spotify.extensions import spotify_registry


registry = MetaRegistry()
registry.include_registry("wordpress", wordpress_registry)
registry.include_registry("get_robots", get_robots_registry)
registry.include_registry("translate", translate_registry)
registry.include_registry("openpeoplesearch", openpeoplesearch_registry)
registry.include_registry("leakcheck", leakcheck_registry)
registry.include_registry("Maigret", Maigret_registry)
registry.include_registry("freecnam", freecnam_registry)
registry.include_registry("spotify", spotify_registry)
