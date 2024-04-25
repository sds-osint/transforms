from modules.leakcheck.extensions import leakcheck_registry

# Import your transforms here
from modules.leakcheck.transforms import leakcheck

if __name__ == "__main__":
    leakcheck_registry.write_local_mtz(command="./venv/bin/python3")
