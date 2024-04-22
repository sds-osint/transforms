from modules.get_robots.extensions import get_robots_registry

# Import your transforms here
from transforms import get_robots

if __name__ == "__main__":
    get_robots_registry.write_local_mtz(command="./venv/bin/python3")