# +=''dD""{}

import copy
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

from Errors import NoWarriorInGame


SplitProces = False
game_result = 'undecided'


class Core:
    def __init__(self, size):  # inaczej
        self.size = size
        self.memory = []
        mnemonic = 'DAT'
        modifier = None
        operands = [[None, 0], [None, 0]]
        comment = None
        instruction = Instruction([mnemonic, modifier, operands, comment])
        for x in range(size):
            copy_of_instuction = copy.deepcopy(instruction)
            self.memory.append(copy_of_instuction)

    def get_size(self):
        return self.size

    def get_memory(self):
        return self.memory

    def visualize(self):  # nie tu na zewnątrz
        # implementacja wizualizacji stanu rdzenia
        # w termonalu
        core_memory = []
        for index, register in enumerate(self.memory):
            core_memory.append((index, register.instruction))
        return core_memory

    # def visualize_2(self):
    #     visualization = Visualize(self.memory())

    def put_instruction_into_core(self, position, instruction):
        self.position = position
        self.memory[position] = instruction

    def set_position(self, new_position):
        self.position = new_position
        if self.position == self.size:
            self.position -= self.size

    def next_position(self):
        self.position += 1
        if self.position == self.size:
            self.position -= self.size

    def get_position(self):
        return self.position

    def execute_instruction(self, position):
        # implementacja wykonywania instrukcji na rdzeniu
        global SplitProces
        self.set_position(position)
        instruction = self.memory[position]
        mnemonic = instruction.mnemonic()
        method = mnemonics[mnemonic](instruction, position, self)
        method.run()

        if SplitProces:
            self.execute_instruction(self.position)
            global SplitProces
            SplitProces = False


# class Visualize:
#     def __init__(self, core) -> None:
#         self.core = core


#     # Tworzymy funkcję, która będzie rysować aktualny stan rdzenia
#     def update(frame):
#         positions = [self.core.get_memory()]
#         plt.cla()
#         plt.scatter(positions[frame][0], positions[frame][1])

#     # Tworzymy obiekt animacji
#     ani = FuncAnimation(plt.gcf(), update, frames=range(len(positions)), repeat=True)

#     # Wyświetlamy animację
#     plt.show()

class Instruction:  # potrzebne
    def __init__(self, instruction):
        self.instruction = instruction

    def mnemonic(self):
        return self.instruction[0]

    def modifier(self):
        return self.instruction[1]

    def operands(self):  # z tego korzystać
        return self.instruction[2]

    def mode_1(self):
        return self.instruction[2][0][0]

    def value_1(self):
        return self.instruction[2][0][1]

    def set_value_1(self, new_value):
        self.instruction[2][0][1] = new_value

    def mode_2(self):
        return self.instruction[2][1][0]

    def value_2(self):
        return self.instruction[2][1][1]

    def set_value_2(self, new_value):
        self.instruction[2][1][1] = new_value

    def comment(self):
        return self.instruction[3]

    def get_instruction(self):
        return self.instruction


class DAT(Instruction):  # w klasach

    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global game_result
        game_result = 'lost'


class MOV(Instruction):  # w klasach
    # kopiuje cały obiekt
    # też funkcję
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        instruction_to_copy = self.core.memory[source_index]
        copy_of_instuction = copy.deepcopy(instruction_to_copy)

        destination_index = calculate_destination_index(self)

        self.core.memory[destination_index] = copy_of_instuction

        if self.instruction.operands()[1][0] == '}':
            self.core.memory[destination_index].set_value_1(
                self.core.memory[destination_index].operands()[0][1]
                + self.instruction.operands()[1][1]
            )

        elif self.instruction.operands()[1][0] == '>':
            self.core.memory[destination_index].set_value_2(
                self.core.memory[destination_index].operands()[1][1]
                + self.instruction.operands()[1][1]
            )

        self.core.next_position()


class ADD(Instruction):  # w klasach
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        instruction_to_change = self.core.memory[
            calculate_destination_index(self)
            ]

        if self.instruction.operands()[0][0] == '#':
            new_value = self.instruction.operands()[0][1] +\
                 instruction_to_change.operands()[1][1]

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class JMP(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.operands()[0][1] + self.position
        self.core.set_position(new_position)


class JMZ(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.operands()[0][1] + self.position
        if new_position == 0:
            self.core.set_position(new_position)
        else:
            self.core.set_position(new_position)


class JMN(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.operands()[0][1] + self.position
        if new_position != 0:
            self.core.set_position(new_position)
        else:
            self.core.set_position(new_position)


class DJN(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.operands()[0][1] + self.position - 1
        if new_position != 0:
            self.core.set_position(new_position)
        else:
            self.core.set_position(new_position)


class SUB(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        instruction_to_change = self.core.memory[
            calculate_destination_index(self)
            ]

        if self.instruction.operands()[0][0] == '#':
            new_value = instruction_to_change.operands()[1][1] -\
                self.instruction.operands()[0][1]

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class NOP(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        self.core.next_position()


class MUL(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        instruction_to_change = self.core.memory[
            calculate_destination_index(self)
            ]

        if self.instruction.operands()[0][0] == '#':
            new_value = instruction_to_change.operands()[1][1] *\
                self.instruction.operands()[0][1]

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class DIV(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        instruction_to_change = self.core.memory[
            calculate_destination_index(self)
            ]

        if self.instruction.operands()[0][0] == '#':
            new_value = instruction_to_change.operands()[1][1] //\
                self.instruction.operands()[0][1]

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class MOD(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        instruction_to_change = self.core.memory[
            calculate_destination_index(self)
            ]

        if self.instruction.operands()[0][0] == '#':
            new_value = instruction_to_change.operands()[1][1] %\
                self.instruction.operands()[0][1]

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class SPL(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.operands()[0][1] + self.position
        self.core.set_position(new_position)
        global SplitProces
        SplitProces = True


class CMP(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        source_index = self.position + self.instruction.operands()[0][1]
        destination_index = self.position + self.instruction.operands()[1][1]

        instruction_1 = self.core.memory[source_index]
        instruction_2 = self.core.memory[destination_index]

        is_mnemonics = bool(instruction_1.mnemonic() == instruction_2.mnemonic())
        is_modifiers = bool(instruction_1.modifier() == instruction_2.modifier())
        is_operands = bool(instruction_1.operands() == instruction_2.operands())
        is_comments = bool(instruction_1.comment() == instruction_2.comment())

        if is_mnemonics and is_modifiers and is_operands and is_comments:
            self.core.set_position(self.position + 1)

        self.core.next_position()


class SEQ(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        source_index = self.position + self.instruction.operands()[0][1]
        destination_index = self.position + self.instruction.operands()[1][1]

        instruction_1 = self.core.memory[source_index]
        instruction_2 = self.core.memory[destination_index]

        is_mnemonics = bool(instruction_1.mnemonic() == instruction_2.mnemonic())
        is_modifiers = bool(instruction_1.modifier() == instruction_2.modifier())
        is_operands = bool(instruction_1.operands() == instruction_2.operands())
        is_comments = bool(instruction_1.comment() == instruction_2.comment())

        if is_mnemonics and is_modifiers and is_operands and is_comments:
            self.core.set_position(self.position + 1)

        self.core.next_position()


class SNE(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        source_index = self.position + self.instruction.operands()[0][1]
        destination_index = self.position + self.instruction.operands()[1][1]

        instruction_1 = self.core.memory[source_index]
        instruction_2 = self.core.memory[destination_index]

        is_mnemonics = bool(instruction_1.mnemonic() != instruction_2.mnemonic())
        is_modifiers = bool(instruction_1.modifier() != instruction_2.modifier())
        is_operands = bool(instruction_1.operands() != instruction_2.operands())
        is_comments = bool(instruction_1.comment() != instruction_2.comment())

        if is_mnemonics and is_modifiers and is_operands and is_comments:
            self.core.set_position(self.position + 1)

        self.core.next_position()


class SLT(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):

        value_1 = self.instruction.operands()[0][1]
        value_2 = self.instruction.operands()[1][1]

        if value_1 < value_2:
            self.core.set_position(self.position + 1)

        self.core.next_position()


def calculate_destination_index(self):
    pointed_index = self.position + self.instruction.operands()[1][1]

    while pointed_index >= self.core.get_size():
        pointed_index -= self.core.get_size()

    pointed_instruction = self.core.memory[pointed_index]

    if self.instruction.operands()[1][0] is None:
        # lub $
        destination_index = self.position + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '*':
        destination_index = self.position + pointed_instruction.operands()[0][1]\
            + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '@':
        destination_index = self.position + pointed_instruction.operands()[1][1]\
            + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '<':

        destination_index = self.position + pointed_instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '>':

        destination_index = self.position + pointed_instruction.operands()[1][1]\
                + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '{':

        destination_index = self.position + pointed_instruction.operands()[0][1]

    elif self.instruction.operands()[1][0] == '}':

        destination_index = self.position + pointed_instruction.operands()[0][1]\
                + self.instruction.operands()[1][1]

    while destination_index >= self.core.get_size():
        destination_index -= self.core.get_size()

    return destination_index


mnemonics = {
    'DAT': DAT,
    'MOV': MOV,
    'ADD': ADD,
    'JMP': JMP,
    'SUB': SUB,
    'MUL': MUL,
    'DIV': DIV,
    'MOD': MOD,
    'JMZ': JMZ,
    'JMN': JMN,
    'DJN': DJN,
    'SPL': SPL,
    'CMP': CMP,
    'SEQ': SEQ,
    'SNE': SNE,
    'SLT': SLT,
    'NOP': NOP
}


class Warrior:  # bez ścieżki
    '''

    '''
    def __init__(self, name, instructions, start_position=0) -> None:
        self.name = name
        self.start_position = start_position
        self.position = start_position
        self.instructions = instructions

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position

    def next_position(self):
        self.position += 1
        return self.position


class Game:
    '''
    '''
    def __init__(self, core, warriors) -> None:
        self._warriors = warriors if warriors else []
        self._core = core if core else []

    def prepare_game(self):
        # inicjuje rdzeń
        # czyta instrukcje z pliku
        # umieszcza je na rdzeniu

        for warrior in self._warriors:

            while warrior.position not in range(self._core.size):
                new_position = warrior.position - self._core.size
                warrior.start_position = warrior.set_position(new_position)

            # start_position = warrior.position
            position = warrior.position

            for instruction in warrior.instructions:
                self._core.put_instruction_into_core(position, instruction)
                # position = warrior.next_position()
                position += 1
                if position == self._core.size:
                    position = warrior.set_position(0)
            # self._core.set_position(warrior.start_position)
            # warrior.set_position(warrior.start_position)

    def play(self):  # nie wszystko na raz
        # wywołuje grę
        round = 1
        print('Starting Core Wars')
        global game_result
        while game_result == 'undecided':
            print(f'Round: {round}')
            if self._warriors:
                for warrior in self._warriors:
                    print(f'Warrior: {warrior.get_name()}')
                    position = warrior.position
                    if position == self._core.size:
                        position = warrior.set_position(0)
                    self._core.execute_instruction(position)
                    warrior.set_position(self._core.get_position())

                    if round > 100:
                        answer = input('Round is over 100. Proceed?(y/n)')
                        if answer == 'y':
                            continue
                        else:
                            game_result = 'drew'
            else:
                raise NoWarriorInGame
            round += 1
        print(f'Game result: Warrior {warrior.get_name()} {game_result}.')
