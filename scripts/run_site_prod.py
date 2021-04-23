"""
run_site_production.py

Serves the site in development mode on port 8000
for testing.

"""

from command import Command

c = Command(['../', 'site', 'unified-makerspace'])
c([['ng', 'serve', '--prod', '--port=8000', '--open']])
