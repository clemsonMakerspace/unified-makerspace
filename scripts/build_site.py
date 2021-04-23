import os
from command import Command

build_path = os.path.join('dist/unified-makerspace')
output_path = os.path.join('%', '..', 'build')

c = Command(['../', 'site', 'unified-makerspace'])
c([['ng', 'build', '--prod'], ['mkdir', '-p', output_path], ['cp','-r', build_path, output_path]])