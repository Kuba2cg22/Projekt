# +=''dD""{}

from math import sqrt

class IncorectPath(Exception):
    pass

class NoWarriorInGame(Exception):
    pass

class WrongPosition(Exception):
    pass

class Core:
    def __init__(self, size):
        self.size = size
        self.memory = [0] * size

    def size(self):
        return self.size

    def visualize(self):
        # implementacja wizualizacji stanu rdzenia
        i = int(sqrt(self.size))
        a = 0
        b = i
        for x in range(i):
            print(self.memory[a:b])
            a += i
            b += i

    def execute_instruction(self, instruction, position):
        # implementacja wykonywania instrukcji na rdzeniu
        # method = getattr(warrior, mnemonic)
        # method(instruction)
        self.memory[position] = instruction



class Instruction:
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


class Operand:
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value

    def mode_value(self):
        return [self.mode, self.value]


class Warrior:
    '''

    '''
    def __init__(self, path, name , position=0) -> None:
        self.name = name
        self.position = position
        self.path = path

    def path(self):
        return self.path

    def name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position


    def instructions(self):
        self._list_of_instructions = []
        try:
            with open(self.path, 'r') as file_handle:
                for line in file_handle:
                    line = line.rstrip().split()
                    mnemonic = line[0][:3]
                    modifier = line[0][3:]
                    try:
                        if ',' in line[1]:
                            line[1] = line[1].replace(',', '')
                        try:
                            int(line[1])
                            mode_1 = None
                            value_1 = line[1]
                        except ValueError:
                            mode_1 = line[1][0]
                            value_1 = line[1][1:]
                        operand_1 = Operand(mode_1, value_1)
                    except IndexError:
                        operand_1 = Operand(None, None)
                    try:
                        try:
                            int(line[2])
                            mode_2 = None
                            value_2 = line[2]
                        except ValueError:
                            mode_2 = line[2][0]
                            value_2 = line[2][1:]
                        operand_2 = Operand(mode_2, value_2)
                    except IndexError:
                        operand_2 = Operand(None, None)
                    operands = [operand_1, operand_2]
                    if ';' in line:
                        comment = ' '.join(line[line.index(';') + 1:])
                    else:
                        comment = None
                    # instruction = Instruction(mnemonic, modifier, operands, comment)
                    self._list_of_instructions.append([mnemonic, modifier, operand_1.mode_value(), operand_2.mode_value(), comment])
        except:
            raise IncorectPath
        return self._list_of_instructions


    def o():
        def DAT(self, instuction):
            pass

        def MOV(self, instuction):
            pass

        def ADD(self, instuction):
            pass

        def SUB(self, instuction):
            pass

        def MUL(self, instuction):
            pass

        def DIV(self, instuction):
            pass

        def MOD(self, instuction):
            pass

        def JMP(self, instuction):
            pass

        def JMZ(self, instuction):
            pass

        def JMN(self, instuction):
            pass

        def DJN(self, instuction):
            pass

        def SPL(self, instuction):
            pass

        def CMP(self, instuction):
            pass

        def SEQ(self, instuction):
            pass

        def SNE(self, instuction):
            pass

        def SLT(self, instuction):
            pass

        def LDP(self, instuction):
            pass

        def STP(self, instuction):
            pass

        def NOP(self, instuction):
            pass


class Game:
    '''
    '''
    def __init__(self, warriors, core) -> None:
        self._warriors = warriors if warriors else []
        self._core = core if core else []

    # def core(self):
    #     return self._core

    def add_warrior(self, warrior):
        self._warriors.append(warrior)

    def remove_warrior(self, warrior):
        if warrior in self._warriors:
            self._warriors.remove(warrior)
        else:
            raise NoWarriorInGame


    def play(self):
        if self._warriors:
            for warrior in self._warriors:
                start_position = warrior.position
                for instruction in warrior.instructions():
                    if start_position == self._core.size:
                        start_position = 0 # a co jak większa pozycja
                    elif start_position not in range(self._core.size):
                        raise WrongPosition
                    # mnemonic = instruction[0]
                    print(instruction)
                    self._core.execute_instruction(instruction, start_position)
                    # method = getattr(warrior, mnemonic)
                    # method(instruction)
                    start_position += 1
                print('Next warrior')
        else:
            raise NoWarriorInGame



warrior_1 = Warrior('wojownik_1.txt','Jaś', 98)
warrior_2 = Warrior('wojownik_2.txt','Asia', 100)
warrior_3 = Warrior('wojownik_3.txt','Kuba', 10)

warriors = [warrior_2]
core_1 = Core(100)

game = Game(warriors, core_1)
# game.add_warrior(warrior_2)
# game.remove_warrior(warrior_1)
core_1.visualize()

game.play()
core_1.visualize()
# # print(warrior_1._list_of_instructions)

# warrior_1 = Warrior('wojownik_1.txt')
# print(warrior_1.instructions())

