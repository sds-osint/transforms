from modules.freecnam.extensions import freecnam_registry

# Import your transforms here
from transforms import get_cnam_person

if __name__ == "__main__":
    freecnam_registry.write_local_mtz(command="./venv/bin/python3")
