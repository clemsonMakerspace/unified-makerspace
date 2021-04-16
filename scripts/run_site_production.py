"""
run_site_production.py

Serves the site in development mode on port 8000
for testing.

"""

import os

current_path = os.path.dirname(os.path.abspath(__file__))
path_to_site = os.path.join('../', 'site', 'unified-makerspace')
command = 'ng serve --prod --port=8000 --open'
os.system(f'cd {current_path} && cd {path_to_site} && {command}')