from command import Command

run_angular = ['../', 'site', 'unified-makerspace']
run_flask = ['cd', '../', 'test_server']

c = Command()
c([['ng', 'serve', '--port=8000', '--open']])

