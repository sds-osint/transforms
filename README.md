# Install

1. Install Python 3.7 or newer
2. Clone repo to a local folder and change into the path 
```
git clone https://github.com/sds-osint/transforms/
cd transforms
```
3. Install dependencies in virtualenv
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Start Docker Compose
```bash
sudo docker compose up -d && sudo docker compose logs -f
```

# Adding transforms to Maltego
There are two ways to add transforms to Maltego: they can be installed as local transforms or they can be added to the TDS. 


## Adding as local transform
1. On the top ribbon under Transforms, select "New Local Transform" and fill out the popup as below: 
2. Give it a memorable Display name and Description and select the appropriate Input entity type. 
3. Command: path to your python executable. For example, "/usr/bin/python3" or "venv/bin/python3" or "python (if it's install on PATH)"
4. Parameters: path to your transorms' python file, without the extension. For example, "project.py local get_robots"
5. Working directory: path to the transforms' folder. For example, "transforms/modules/get_robots/transforms/get_robots"

## Using the TDS
Maltego has a public Transform server available at https://public-tds.paterva.com/. Must have an account and have a server available. 

### Creating the transform in the TDS
1. Select Seeds and create a new seed. Give it a memorable name. 
2. Select Transforms and Add transform
3. Give the transform a memorable name and display
4. Add the transform URL. This will be either the IP address or domain (if there is one) that points to your Maltego server, followed by the path to the transform. That path is initially printed out when starting the docker container. For example, "https://tds.yourdomain.com/run/get-robots" or "http://123.456.78.9/run/get-robots". 
5. Select the most fitting Input Entity and any relevant Output entities. 
6. Add it to the previously created seed. 

### Adding the transform
1. At the bottom of the Maltego Transform Hub page under Internal Hub Items, click the big Plus sign. 
2. Add the Transform Name and Transform UI Display to the ID and Name fields in the Add Transform Seed window. 
3. Copy the transform seed URL from the public TDS page and put it in the Seed URL box. 
4. Fill out the rest of the fields as best appropriate. 
5. Let it process and then install the transform. 




# Creating Modules

We advise the following structure. In any case, the transforms **need** to be in a dir called `transforms`.

```
modules
└── <module_name>
    └── transforms
        └── <transform_name>.py
```

You can optionally specify a `whitelist` or `blacklist` in `project.py`. To disable them set them to `None`

## Create a module
To create a module 

1. use the python script `create_module.py`. The script needs following positional arguments: name author owner.

```shell
usage: create_module.py [-h] name author owner

positional arguments:
  name        The module name
  author      your email address, alias or Fullname
  owner       You, or the organization you write this module for
```

e.g.

```shell
source venv/bin/activate
python3 create_module.py my_module me@myself.com "Me Inc."
```

2. Edit in the top-level of the `extensions.py` file and add following lines:   
```
from modules.{name}.extensions import {name}_registry

registry.include_registry("{name}", {name}_registry
```

e.g. name = 'cisa'

```
from meta_registry import MetaRegistry
from modules.cisa.extensions import cisa_registry

registry = MetaRegistry()
registry.include_registry("cisa", cisa_registry)
```


