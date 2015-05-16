from core import tools
import matplotlib.pyplot as plt

data = tools.convert_to_numpy("storage/progenitor.txt")

numclones = tools.count_clones(data)

alpha, omega, mup, p, num_of_clones, bone_capacity = 0.01, 0.2, 0.2, 1.0, 100, 1000
equilclones = tools.steady_clones_progenitors(alpha, omega, mup, p, num_of_clones, bone_capacity)

plt.plot(numclones)
plt.axhline(equilclones, c='g')
plt.show()