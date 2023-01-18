import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Tworzymy listę z pozycjami wojowników
positions = [[1, 2], [3, 4], [5, 6], [7, 8]]

# Tworzymy funkcję, która będzie rysować aktualny stan rdzenia
def update(frame):
    plt.cla()
    plt.scatter(positions[frame][0], positions[frame][1])

# Tworzymy obiekt animacji
ani = FuncAnimation(plt.gcf(), update, frames=range(len(positions)), repeat=True)

# Wyświetlamy animację
plt.show()
