import matplotlib.animation as animation
import matplotlib.pyplot as plt
import time

lista = [1,2,3,4,5,6,7]




def update_graph(num):
    plt.clf()
    plt.bar(range(len(lista)), lista)
    plt.title('Lista po iteracji {}'.format(num))




for x in range(19):
    lista.append(x)
    update_graph(x)
    plt.show(block=False)
    plt.pause(1)
    plt.clf()