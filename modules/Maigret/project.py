from modules.Maigret.extensions import Maigret_registry

# Import your transforms here
from modules.Maigret.transforms import Maigret

if __name__ == "__main__":
    Maigret_registry.write_local_mtz(command="./venv/bin/python3")
