from modules.wordpress.extensions import wordpress_registry

# Import your transforms here
from transforms import *

if __name__ == "__main__":
    wordpress_registry.write_local_mtz(command="./venv/bin/python3")