from modules.openpeoplesearch.extensions import openpeoplesearch_registry

# Import your transforms here
from transforms import OpenPeopleSearch

if __name__ == "__main__":
    openpeoplesearch_registry.write_local_mtz(command="./venv/bin/python3")