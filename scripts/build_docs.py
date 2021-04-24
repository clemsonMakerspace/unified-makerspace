"""
make_docs.py

Compiles API documentation to PDF. Outputs to /build
in root directory.

"""

import os
from command import Command

# settings
output_type = "html"
file_name = "theunifiedmakerspace.pdf"
build_path = os.path.join("build", "latex", file_name)
output_path = os.path.join('%', '..', 'build')

# run
c = Command(exec_path=["../","api", "docs"])
c([['make', output_type], ['mkdir', '-p', output_path], ['cp', build_path, output_path]])
