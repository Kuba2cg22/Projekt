# +=''dD""{}

class IncorectPath(Exception):
    pass

class NoWarriorInGame(Exception):
    pass

class Core:
    def __init__(self, size):
        self.memory = [0] * size

    def visualize(self):
        # implementacja wizualizacji stanu rdzenia
        pass

    def execute_instruction(self, instruction):
        # implementacja wykonywania instrukcji na rdzeniu
        # method = getattr(warrior, mnemonic)
        # method(instruction)
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


class Operand:
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value

    def mode_value(self):
        return [self.mode, self.value]


class Warrior:
    '''

    '''
    def __init__(self, path) -> None:
        self._list_of_instructions = []
        # try:
        with open(path, 'r') as file_handle:
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
                instruction = Instruction(mnemonic, modifier, operands, comment)
                # Core.execute_instruction(instruction)

                self._list_of_instructions.append([mnemonic, modifier, [operand_1.mode_value(), operand_2.mode_value()], comment])
        # except:
        #     raise IncorectPath


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
                for instruction in warrior._list_of_instructions:
                    mnemonic = instruction[0]
                    print(instruction)
                    method = getattr(warrior, mnemonic)
                    method(instruction)
                print('Next warrior')
        else:
            raise NoWarriorInGame



# warrior_1 = Warrior('wojownik_1.txt')
# warrior_2 = Warrior('wojownik_2.txt')
warrior_3 = Warrior('wojownik_3.txt')

warriors = [warrior_3]
core_1 = []

game = Game(warriors, core_1)
# game.add_warrior(warrior_2)
# game.remove_warrior(warrior_1)


game.play()

# print(warrior_1._list_of_instructions)