# +=''dD""{}

core_1 = []


class Warrior:
    '''

    '''
    def __init__(self, path) -> None:
        self._list_of_instructions = []
        with open(path, 'r') as file_handle:
            for line in file_handle:
                line = line.rstrip().split()
                for index, element in enumerate(line):
                    if element == ';':
                        line = line[0:index]  # removes comments
                    if ',' in element:
                        line[index] = element.replace(',', '')
                self._list_of_instructions.append(line)

    # def instructions(self):
    #     for instruction in self._list_of_instructions:
    #         return instruction

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

    def play(self):
        for warrior in warriors:
            for instruction in warrior._list_of_instructions:
                mnemonic = instruction[0]
                print(instruction, mnemonic)
                method = getattr(warrior, mnemonic)
                method(instruction)
            print('Next warrior')


warrior_1 = Warrior('wojownik_1.txt')
warrior_2 = Warrior('wojownik_2.txt')
warriors = [warrior_1, warrior_2]

game = Game(warriors, core_1)

game.play()
# i = warrior_1.instructions()

# print(i)
