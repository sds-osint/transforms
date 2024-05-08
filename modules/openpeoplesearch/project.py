from modules.openpeoplesearch.extensions import openpeoplesearch_registry

# Import your transforms here
from transforms import ops_company, ops_email, ops_person, ops_phone

if __name__ == "__main__":
    openpeoplesearch_registry.write_local_mtz(command="./venv/bin/python3")