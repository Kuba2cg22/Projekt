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
        self.memory = [['NOP', '', [None, None], [None, None], None]] * size



    def size(self):
        return self.size

    def visualize(self):
        # implementacja wizualizacji stanu rdzenia
        for index, register in enumerate(self.memory):
            print(index, register)


    def put_instruction_into_core(self, instruction, position):
        self.position = position
        self.memory[position] = instruction

    def next_position(self):
        self.position += 1


    def execute_instructions(self):
        # implementacja wykonywania instrukcji na rdzeniu

        for register in self.memory:
            mnemonic = register[0]
            modifier = register[1]
            mode_1 ,value_1 = register[2]
            mode_2 ,value_2 = register[3]
            method = getattr(self, mnemonic)
            method(register)

    def DAT(self):
        pass

    def MOV(self, register):
        modifier = register[1]
        mode_1 ,value_1 = register[2]
        mode_2 ,value_2 = register[3]
        self.memory[3] = self.memory[2]


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

    def NOP(self, register):
        pass




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

    def run_instruction(self):
        pass


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
        self._list_of_raw_instructions = []
        try:
            with open(self.path, 'r') as file_handle:
                for line in file_handle:
                    line = line.rstrip()
                    # self._list_of_raw_instructions.append(line)
                    line = line.split()
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
                actual_position = start_position
                for instruction in warrior.instructions():
                    if actual_position == self._core.size:
                        actual_position = 0
                    elif actual_position not in range(self._core.size):
                        raise WrongPosition
                    print(instruction)
                    self._core.put_instruction_into_core(instruction, actual_position)
                    actual_position += 1
                self._core.execute_instructions()
                print('Next warrior')
        else:
            raise NoWarriorInGame



warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
warrior_4 = Warrior('wojownik_4.txt','Kuba', 10)

warriors = [warrior_2]
core_1 = Core(10)

game = Game(warriors, core_1)
# game.add_warrior(warrior_2)
# game.remove_warrior(warrior_1)
core_1.visualize()

game.play()
core_1.visualize()
# # print(warrior_1._list_of_instructions)

# warrior_1 = Warrior('wojownik_1.txt')
# print(warrior_1.instructions())

