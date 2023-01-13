# +=''dD""{}

# from math import sqrt

class IncorectPath(Exception):
    pass


class NoWarriorInGame(Exception):
    pass


class WrongPosition(Exception):
    pass


class Core:
    def __init__(self, size):
        self.size = size
        self.memory = [
            ['DAT', None, [[None, None], [None, None]], None]
            ] * size

    def get_size(self):
        return self.size

    def visualize(self):  # nie tu na zewnątrz
        # implementacja wizualizacji stanu rdzenia
        for index, register in enumerate(self.memory):
            print(index, register)

    def put_instruction_into_core(self, position, instruction):
        self.position = position
        try:
            self.memory[position] = instruction
        except IndexError:
            print('Wrong start position')

    def next_position(self):
        self.position += 1

    def execute_instruction(self, position):
        # implementacja wykonywania instrukcji na rdzeniu
        instruction = self.memory[position]
        mnemonic = instruction.mnemonic()
        method = getattr(mnemonic, 'run')
        method(instruction, position)


        # for index, register in enumerate(self.memory):  # nie tak
        #     method = getattr(self, mnemonic)
        #     method(register, index)



    def DAT(self):  # w klasach
        pass

    def MOV(self, register, index):
        modifier = register[1]
        mode_1 ,value_1 = register[2]
        mode_2 ,value_2 = register[3]
        destination_index = index + int(value_2)
        source_index = index + int(value_1)
        while destination_index >= Core.size(self):
            destination_index -= Core.size(self)
        while source_index >= Core.size(self):
            source_index -= Core.size(self)
        self.memory[destination_index] = self.memory[source_index]

    def ADD(self):
        pass

    def SUB(self):
        pass

    def MUL(self):
        pass

    def DIV(self):
        pass

    def MOD(self):
        pass

    def JMP(self):
        pass

    def JMZ(self):
        pass

    def JMN(self):
        pass

    def DJN(self):
        pass

    def SPL(self):
        pass

    def CMP(self):
        pass

    def SEQ(self):
        pass

    def SNE(self):
        pass

    def SLT(self):
        pass

    def LDP(self):
        pass

    def STP(self):
        pass

    def NOP(self, register, index):
        pass


class Instruction:  # potrzebne
    def __init__(self, instruction):
        self.instruction = instruction

    def mnemonic(self):
        return self.instruction[0]

    def modifier(self):
        return self.instruction[1]

    def operands(self):
        return self.instruction[2]

    def comment(self):
        return self.instruction[3]

    def run_instruction(self):
        pass


class DAT(Instruction):  # w klasach
    def __init__(self, instruction):
        super().__init__(instruction)


class MOV(Instruction):  # w klasach
    def __init__(self, instruction):
        super().__init__(instruction)


        # modifier = instruction.
        # mode_1 ,value_1 = register[2]
        # mode_2 ,value_2 = register[3]
        # destination_index = index + int(value_2)
        # source_index = index + int(value_1)
        # while destination_index >= Core.size(self):
        #     destination_index -= Core.size(self)
        # while source_index >= Core.size(self):
        #     source_index -= Core.size(self)
        # self.memory[destination_index] = self.memory[source_index]


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
                mode_1, value_1 = None, self.line[1]
            except ValueError:
                mode_1, value_1 = self.line[1][0], self.line[1][1:]
        except IndexError:
            mode_1, value_1 = None, None
        operand_1 = [mode_1, value_1]

        try:
            self.line[2]
            try:
                int(self.line[2])
                mode_2, value_2 = None, self.line[2]
            except ValueError:
                mode_2, value_2 = self.line[2][0], self.line[2][1:]
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
            self._list_of_instructions.append(
                instruction
                )

        return self._list_of_instructions


class Warrior:  # bez ścieżki
    '''

    '''
    def __init__(self, name, position=0) -> None:
        self.name = name
        self.position = position

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
    def __init__(self, core, ready_warriors) -> None:
        self._ready_warriors = ready_warriors if ready_warriors else []
        self._core = core if core else []
        self.result = 'undecided'

    def prepare_game(self):
        # inicjuje rdzeń
        # czyta instrukcje z pliku
        # umieszcza je na rdzeniu

        for ready_warrior in self._ready_warriors:

            warrior = ready_warrior[0]
            instructions = ready_warrior[1]
            start_positon = warrior.position
            position = warrior.position

            for instruction in instructions:
                while position not in range(self._core.size):
                    new_position = warrior.position - self._core.size
                    position = warrior.set_position(new_position)
                print(instruction)
                self._core.put_instruction_into_core(position, instruction)
                position = warrior.next_position()
                if position == self._core.size:
                    position = warrior.set_position(0)
            warrior.set_position(start_positon)

    def play(self):  # nie wszystko na raz
        # wywołuje grę
        round = 1
        print('Starting Core Wars')
        while self.result == 'undecided':
            print(f'Round: {round}')
            if self._ready_warriors:
                for ready_warrior in self._ready_warriors:
                    warrior = ready_warrior[0]
                    start_position = warrior.position
                    actual_position = start_position
                    # aż nie przerwie
                    self._core.execute_instruction(actual_position)
                    print('Next warrior')
                    if round >= 100:
                        answer = input('Its round 100. Proceed?(y/n)')
                        if answer == 'y':
                            continue
                        else:
                            self.result = 'Its draw'
            else:
                raise NoWarriorInGame
        print(f'Game result: {self.result}')


warrior_1 = Warrior('Jakub', 0)
warrior_1_instructions = Read_from_file('wojownik_1.txt')
instructions_1 = warrior_1_instructions.get_instructions()
ready_warrior_1 = [warrior_1, instructions_1]

warrior_3 = Warrior('Kuba', 5)
warrior_3_instructions = Read_from_file('wojownik_3.txt')
instructions_3 = warrior_3_instructions.get_instructions()
ready_warrior_3 = [warrior_3, instructions_3]

ready_warriors = [ready_warrior_3]

core_1 = Core(10)
core_1.visualize()

game_1 = Game(core_1, ready_warriors)

game_1.prepare_game()

core_1.visualize()

game_1.play()
