from modules.translate.extensions import translate_registry

# Import your transforms here
from transforms import translate

if __name__ == "__main__":
    translate_registry.write_local_mtz(command="./venv/bin/python3")
