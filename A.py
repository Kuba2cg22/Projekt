# +=''dD""{}


lista = [1, 2, 3, 4, 5]

# for i, x in enumerate(lista):
#     if x == 4:
#         lista = lista[0:i]

# print(lista)

def func():
    for index, element in enumerate(lista):
        is_end = bool(index + 1 == len(lista))
        print(element, index, is_end)
        if is_end:
            func()


# func()

# i = 757


# while i not in range(len(lista)):
#     i -= len(lista)

# print(i)

# b = 'ASW;'

# print(b.replace(';', ''))




# def NOP():
#     print(1)

# a = 'NOP'

# globals()[a]()

c = [1, 2]

u, i = c

print(type(c)==list)
