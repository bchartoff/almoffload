import logging, sys
logging.basicConfig(stream=sys.stderr)

import os

import sys
sys.path.append('/var/www/html')
from almoffload import app as application
