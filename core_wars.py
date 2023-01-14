# +=''dD""{}


class IncorectPath(Exception):
    pass


class NoWarriorInGame(Exception):
    pass


class WrongPosition(Exception):
    pass


class WarriorLosses(Exception):
    pass


class Core:
    def __init__(self, size):
        self.size = size
        mnemonic = 'DAT'
        modifier = None
        operands = [[None, None], [None, None]]
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

    def next_position(self):
        self.position += 1

    def get_position(self):
        return self.position

    def execute_instruction(self, position):
        # implementacja wykonywania instrukcji na rdzeniu
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

    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        if self.instruction.mode_1() is None and self.instruction.mode_2() is None:
            destination_index = self.position + self.instruction.value_2()
            source_index = self.position + self.instruction.value_1()
            while destination_index >= self.core.get_size():  # tuu
                destination_index -= self.core.get_size()
            while source_index >= self.core.get_size():
                source_index -= self.core.get_size()

            self.core.memory[destination_index] = self.core.memory[source_index]

        if self.instruction.mode_2() == '@':
            source_index = self.position + self.instruction.value_1()
            second_instruction = self.core.memory[source_index]

            destination_index = self.position + second_instruction.value_2() + self.instruction.value_2()

            while destination_index >= self.core.get_size():  # tuu
                destination_index -= self.core.get_size()
            while source_index >= self.core.get_size():
                source_index -= self.core.get_size()

            self.core.memory[destination_index] = self.core.memory[source_index]

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

        second_instruction = self.core.memory[destination_index]

        if self.instruction.mode_1() == '#':  # czego ustawia wszystko
            second_instruction.set_value_2(
                self.instruction.value_1() + second_instruction.value_2()
                )

        self.core.next_position()


class JMP(Instruction):
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        new_position = self.instruction.value_1() + self.position
        self.core.set_position(new_position)


def i():


    class SUB(Instruction):
        pass


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
    # 'SUB': SUB,
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


class Read_from_file:
    def __init__(self, path) -> None:
        self.path = path
        self.lines = []
        try:
            with open(self.path, 'r') as file_handle:
                for line in file_handle:
                    self.line = line.rstrip().split()
                    self.lines.append(self.line)
        except:
            raise IncorectPath

    def get_mnemonic(self):
        mnemonic = self.line[0][:3]
        return mnemonic

    def get_modifier(self):
        modifier = self.line[0][3:]
        if len(modifier) == 0:
            modifier = None
        return modifier

    def get_operands(self):
        try:
            if ',' in self.line[1]:
                self.line[1] = self.line[1].replace(',', '')
            try:
                int(self.line[1])
                mode_1, value_1 = None, int(self.line[1])
            except ValueError:
                mode_1, value_1 = self.line[1][0], int(self.line[1][1:])
        except IndexError:
            mode_1, value_1 = None, None
        operand_1 = [mode_1, value_1]

        try:
            self.line[2]
            try:
                int(self.line[2])
                mode_2, value_2 = None, int(self.line[2])
            except ValueError:
                mode_2, value_2 = self.line[2][0], int(self.line[2][1:])
        except IndexError:
            mode_2, value_2 = None, None
        operand_2 = [mode_2, value_2]

        operands = [operand_1, operand_2]
        return operands

    def get_comment(self):
        if ';' in self.line:
            comment = ' '.join(self.line[self.line.index(';') + 1:])
        else:
            comment = None
        return comment

    def get_instructions(self):
        self._list_of_instructions = []
        for self.line in self.lines:
            mnemonic = self.get_mnemonic()
            modifier = self.get_modifier()
            operands = self.get_operands()
            comment = self.get_comment()
            instruction = Instruction([mnemonic, modifier, operands, comment])
            self._list_of_instructions.append(instruction)

        return self._list_of_instructions


class Warrior:  # bez ścieżki
    '''

    '''
    def __init__(self, name, instructions, position=0) -> None:
        self.name = name
        self.position = position
        self.instructions = instructions

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position
        return self.position

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
                start_position = warrior.set_position(new_position)

            start_position = warrior.position
            position = warrior.position

            for instruction in warrior.instructions:
                self._core.put_instruction_into_core(position, instruction)
                position = warrior.next_position()
                if position == self._core.size:
                    position = warrior.set_position(0)
            self._core.set_position(start_position)
            warrior.set_position(start_position)

    def play(self):  # nie wszystko na raz
        # wywołuje grę
        round = 1
        print('Starting Core Wars')
        while self.result == 'undecided':
            print(f'Round: {round}')
            if self._warriors:
                for warrior in self._warriors:
                    print(f'Warrior: {warrior.get_name()}')
                    warrior.set_position(self._core.get_position())
                    position = warrior.position
                    if position == self._core.size:
                        position = warrior.set_position(0)
                    try:
                        self._core.execute_instruction(position)
                        # aktualizacja pozycji
                    except WarriorLosses:
                        self.result = f'Warrior {warrior.get_name()} lost'
                        break  # ?
                    # position = warrior.next_position()  # usunęć i zmieniać  w core
                    if round > 50:
                        answer = input('Round is over 50. Proceed?(y/n)')
                        if answer == 'y':
                            continue
                        else:
                            self.result = 'Its draw'
                            break  # ?
            else:
                raise NoWarriorInGame
            round += 1
        print(f'Game result: {self.result}')
