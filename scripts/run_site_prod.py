"""
run_site_prod.py

Serves the site in production mode on port 8000.

"""

from command import Command

c = Command(['../', 'site', 'unified-makerspace'])
c([['ng', 'serve', '--prod', '--port=8000', '--open']])
