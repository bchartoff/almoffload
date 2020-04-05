activate_this = '/var/www/html/almoffload/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import logging, sys
logging.basicConfig(stream=sys.stderr)

import os

import sys
sys.path.append('/var/www/html')
from almoffload import app as application
