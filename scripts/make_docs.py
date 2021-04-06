

import os

path = os.path.join("../","api", "docs")
output = "latexpdf"
filename = "theunifiedmakerspace.pdf"
output_path = os.path.join(path, "build", "latex", filename)
os.system(f"cd {path} && make {output}")
os.system(f"cp {output_path} $HOME/my/desktop")




