from core import tools
import numpy as np

data = tools.convert_to_numpy("serious.txt")

print tools.count_clones(data)
