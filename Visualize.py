
core_memory = []


def visualize(memory):
    for index, register in enumerate(memory):
        yield (index, register.instruction)
