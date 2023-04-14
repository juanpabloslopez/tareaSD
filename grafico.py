import matplotlib.pyplot as plt

# Leer los tiempos del archivo
with open("tiempos.txt", "r") as f:
    tiempos = [float(line.strip()) for line in f]

# Crear el gráfico
plt.plot(tiempos)
plt.xlabel("Número de ejecución")
plt.ylabel("Tiempo (segundos)")
plt.title("Tiempos de ejecución")
plt.show()
