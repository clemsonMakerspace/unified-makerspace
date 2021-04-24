"""
run_site_dev.py

Serves the site in development mode on port 7000,
using the mock backend.

"""


from command import Command


c = Command(['../', 'site', 'unified-makerspace'])
c([['npm', 'run', 'server', '&>/dev/null'], ['ng', 'serve', '--port=8000', '--open']])

