import logging, sys
logging.basicConfig(stream=sys.stderr)

import os

import sys
sys.path.append('/var/www/apache2')
from almoffload import app as application
