from core import tools
import matplotlib.pyplot as plt

data = tools.convert_to_numpy("storage/progenitor.txt")

totalcells = data.sum(axis=0)
numclones = tools.count_clones(data)

alpha, omega, mup, p, num_of_clones, bone_capacity = 0.05, 0.2, 0.2, 1.0, 1000, 1000
equilclones = tools.steady_clones_progenitors(alpha, omega, mup, p, num_of_clones, bone_capacity)
equiltotal = tools.steady_total_progenitors(alpha, omega, mup, p, num_of_clones, bone_capacity)

plt.figure()
plt.plot(numclones)
plt.axhline(equilclones, c='g', linestyle='--')

plt.figure()
plt.plot(totalcells)
plt.axhline(equiltotal, c='g', linestyle='--')

plt.show()