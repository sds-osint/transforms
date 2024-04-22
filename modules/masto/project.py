from modules.masto.extensions import masto_registry

# Import your transforms here
from modules.masto.transforms import masto_instances

if __name__ == "__main__":
    masto_registry.write_local_mtz(command="./venv/bin/python3")
