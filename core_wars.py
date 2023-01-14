# +=''dD""{}

import copy

from Errors import (
    NoWarriorInGame,
    WarriorLosses
)


class Core:
    def __init__(self, size):
        self.size = size
        mnemonic = 'DAT'
        modifier = None
        operands = [[None, 0], [None, 0]]
        comment = None
        instruction = Instruction([mnemonic, modifier, operands, comment])
        self.memory = [instruction] * size

    def get_size(self):
        return self.size

    def visualize(self):  # nie tu na zewnątrz
        # implementacja wizualizacji stanu rdzenia
        core_memory = []
        for index, register in enumerate(self.memory):
            core_memory.append((index, register.instruction))
        return core_memory

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
        self.set_position(position)
        instruction = self.memory[position]
        mnemonic = instruction.mnemonic()
        method = mnemonics[mnemonic](instruction, position, self)  # czy można samo self
        method.run()


class Instruction:  # potrzebne
    def __init__(self, instruction):
        self.instruction = instruction

    def mnemonic(self):
        return self.instruction[0]

    def modifier(self):
        return self.instruction[1]

    def operands(self):
        return self.instruction[2]

    def mode_1(self):
        return self.instruction[2][0][0]

    def value_1(self):
        return self.instruction[2][0][1]

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
        raise WarriorLosses


class MOV(Instruction):  # w klasach
    # kopiuje cały obiekt
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        source_index = self.position + self.instruction.value_1()

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        instruction_to_copy = self.core.memory[source_index]
        copy_of_instuction = copy.deepcopy(instruction_to_copy)

        if self.instruction.mode_1() is None and self.instruction.mode_2() is None:  # lub $
            destination_index = self.position + self.instruction.value_2()
            # source_index = self.position + self.instruction.value_1()

            while destination_index >= self.core.get_size():
                destination_index -= self.core.get_size()

            self.core.memory[destination_index] = copy_of_instuction

        elif self.instruction.mode_2() == '*':
            destination_index = self.position + instruction_to_copy.value_1()\
                + self.instruction.value_2()

            while destination_index >= self.core.get_size():
                destination_index -= self.core.get_size()

            self.core.memory[destination_index] = copy_of_instuction

        elif self.instruction.mode_2() == '@':

            destination_index = self.position + instruction_to_copy.value_2()\
                + self.instruction.value_2()

            while destination_index >= self.core.get_size():
                destination_index -= self.core.get_size()

            self.core.memory[destination_index] = copy_of_instuction
            # nowy obiekt

        elif self.instruction.mode_2() == '<':

            needed_instruction = self.core.memory[
                self.position + instruction_to_copy.value_2()
                ]

            destination_index = self.position + instruction_to_copy.value_2()\
                + needed_instruction.value_2()

            while destination_index >= self.core.get_size():
                destination_index -= self.core.get_size()

            self.core.memory[destination_index] = copy_of_instuction

        self.core.next_position()


class ADD(Instruction):  # w klasach
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        destination_index = self.position + self.instruction.value_2()

        while destination_index >= self.core.get_size():
            destination_index -= self.core.get_size()

        instruction_to_copy = self.core.memory[destination_index]

        if self.instruction.mode_1() == '#':  # czego ustawia wszystko
            new_value = self.instruction.value_1() + instruction_to_copy.value_2()
            instruction_to_copy.set_value_2(new_value)

        self.core.next_position()


class JMP(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.value_1() + self.position
        self.core.set_position(new_position)


class SUB(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        self.core.next_position()


def i():




    class MUL(Instruction):
        pass


    class DIV(Instruction):
        pass


    class MOD(Instruction):
        pass




    class JMZ(Instruction):
        pass


    class JMN(Instruction):
        pass


    class DJN(Instruction):
        pass


    class SPL(Instruction):
        pass


    class CMP(Instruction):
        pass


    class SEQ(Instruction):
        pass


    class SNE(Instruction):
        pass


    class SLT(Instruction):
        pass


    class LDP(Instruction):
        pass


    class STP(Instruction):
        pass


    class NOP(Instruction):
        pass


mnemonics = {
    'DAT': DAT,
    'MOV': MOV,
    'ADD': ADD,
    'JMP': JMP,
    'SUB': SUB,
    # 'MUL': MUL,
    # 'DIV': DIV,
    # 'MOD': MOD,
    # 'JMZ': JMZ,
    # 'JMN': JMN,
    # 'DJN': DJN,
    # 'SPL': SPL,
    # 'CMP': CMP,
    # 'SEQ': SEQ,
    # 'SNE': SNE,
    # 'SLT': SLT,
    # 'LDP': LDP,
    # 'STP': STP,
    # 'NOP': NOP
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
        # return self.position

    def next_position(self):
        self.position += 1
        return self.position


class Game:
    '''
    '''
    def __init__(self, core, warriors) -> None:
        self._warriors = warriors if warriors else []
        self._core = core if core else []
        self.result = 'undecided'

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
        while self.result == 'undecided':
            print(f'Round: {round}')
            if self._warriors:
                for warrior in self._warriors:
                    print(f'Warrior: {warrior.get_name()}')
                    position = warrior.position
                    if position == self._core.size:
                        position = warrior.set_position(0)
                    try:
                        self._core.execute_instruction(position)
                        # aktualizacja pozycji
                    except WarriorLosses:
                        self.result = f'Warrior {warrior.get_name()} lost'
                        break  # ?
                    warrior.set_position(self._core.get_position())
                    # position = warrior.next_position()  # usunęć i zmieniać  w core
                    if round > 100:
                        answer = input('Round is over 100. Proceed?(y/n)')
                        if answer == 'y':
                            continue
                        else:
                            self.result = 'Its draw'
                            break  # ?
            else:
                raise NoWarriorInGame
            round += 1
        print(f'Game result: {self.result}')
