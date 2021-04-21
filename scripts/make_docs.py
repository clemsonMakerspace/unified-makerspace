"""
make_docs.py

Compiles API documentation to PDF.

"""

# todo refactor (create command class?)

import os

output = "latexpdf"
filename = "theunifiedmakerspace.pdf"

path = os.path.join("../","api", "docs")

output_path = os.path.join(path, "build", "latex", filename)
os.system(f"cd {path} && make {output}")
os.system(f"cp {output_path} $p")
