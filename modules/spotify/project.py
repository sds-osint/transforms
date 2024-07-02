import sys
import transforms
from maltego_trx.handler import handle_run
from maltego_trx.registry import register_transform_classes
from maltego_trx.server import app as application
from transforms import *
import os

register_transform_classes(transforms)

if __name__ == '__main__':
    if '--debug' in sys.argv:
        os.environ['FLASK_ENV'] = 'development'
        application.run(debug=True, host='0.0.0.0', port=8091)
    else:
        handle_run(__name__, sys.argv, application)