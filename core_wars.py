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
        self.memory = [['DAT', '', [None, None], [None, None], None]] * size

    def get_size(self):
        return self.size

    def visualize(self):  # nie tu na zewnątrz
        # implementacja wizualizacji stanu rdzenia
        for index, register in enumerate(self.memory):
            print(index, register)

    def put_instruction_into_core(self, position, instruction):
        self.position = position
        self.memory[position] = instruction

    def next_position(self):
        self.position += 1

    def execute_instructions(self):
        # implementacja wykonywania instrukcji na rdzeniu

        for index, register in enumerate(self.memory):  # nie tak
            mnemonic = register[0]
            modifier = register[1]
            mode_1 ,value_1 = register[2]
            mode_2 ,value_2 = register[3]
            method = getattr(self, mnemonic)
            method(register, index)

# class DAT(Instruction):  # w klasach
#     pass

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
    def __init__(self, mnemonic, modifier, operands, comment):
        self.mnemonic = mnemonic
        self.modifier = modifier
        self.operands = operands
        self.comment = comment

    def mnemonic(self):
        return self.mnemonic

    def modifier(self):
        return self.modifier

    def operands(self):
        return self.operands

    def comment(self):
        return self.comment

    def run_instruction(self):
        pass


# class Operand:
#     def __init__(self, mode, value):
#         self.mode = mode
#         self.value = value

#     def mode_value(self):
#         return [self.mode, self.value]

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
        try:
            self.line[2]
            try:
                int(self.line[2])
                mode_2, value_2 = None, self.line[2]
            except ValueError:
                mode_2, value_2 = self.line[2][0], self.line[2][1:]
        except IndexError:
            mode_2, value_2 = None, None
        operand_1 = [mode_1, value_1]
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
            self._list_of_instructions.append(
                [mnemonic, modifier, operands, comment]
                )
        # instruction = Instruction(mnemonic, modifier, operands, comment)
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


class Game:
    '''
    '''
    def __init__(self, warriors, core) -> None:
        self._warriors = warriors if warriors else []
        self._core = core if core else []

    def prepare_game(self):
        # inicjuje rdzeń
        # czyta instrukcje z pliku
        # umieszcza je na rdzeniu
        pass

    def play(self):  # nie wszystko na raz
        # wywołuje grę
        if self._warriors:
            for warrior in self._warriors:
                start_position = warrior.position
                actual_position = start_position
                for instruction in warrior.instructions():
                    if actual_position == self._core.size:
                        actual_position = 0
                    elif actual_position not in range(self._core.size):
                        raise WrongPosition
                    print(instruction)
                    self._core.put_instruction_into_core(instruction, actual_position)
                    actual_position += 1
                self._core.execute_instructions()  # aż nie przerwie
                self._core.execute_instructions()
                print('Next warrior')
        else:
            raise NoWarriorInGame


# warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
# warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
# warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
# warrior_4 = Warrior('wojownik_4.txt','Kuba', 10)

# warriors = [warrior_2]
# core_1 = Core(4)

# game = Game(warriors, core_1)
# # game.add_warrior(warrior_2)
# # game.remove_warrior(warrior_1)
# core_1.visualize()

# game.play()
# core_1.visualize()
# # print(warrior_1._list_of_instructions)

# warrior_1 = Warrior('wojownik_1.txt')
# print(warrior_1.instructions())

plik = Read_from_file('wojownik_3.txt')
inst = plik.get_instructions()
for i in inst:
    print(i)