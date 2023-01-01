# +=''dD""{}

class IncorectPath(Exception):
    pass

class NoWarriorInGame(Exception):
    pass
    


class Warrior:
    '''

    '''
    def __init__(self, path) -> None:
        self._list_of_instructions = []
        try:
            with open(path, 'r') as file_handle:
                for line in file_handle:
                    line = line.rstrip().split()
                    for index, element in enumerate(line):
                        if element == ';':
                            line = line[0:index]  # removes comments
                        if ',' in element:
                            line[index] = element.replace(',', '')
                    self._list_of_instructions.append(line)
        except:
            raise IncorectPath


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
                    print(instruction, mnemonic)
                    method = getattr(warrior, mnemonic)
                    method(instruction)
                print('Next warrior')
        else:
            raise NoWarriorInGame



# warrior_1 = Warrior('wojownik_1.txt')
# warrior_2 = Warrior('wojownik_2.txt')
# warriors = [warrior_1]
# core_1 = []

# game = Game(warriors, core_1)
# # game.add_warrior(warrior_2)
# # game.remove_warrior(warrior_1)


# game.play()

# print(warrior_1._list_of_instructions)