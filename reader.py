# from Errors import IncorectPath

from core_wars import Instruction

from Errors import (
    IncorrectMnemonicsError,
    IncorrectModifiersError,
    IncorrectOperandsError,
    IncorrectValueError
)

list_of_mnemonics = [
    'DAT', 'MOV', 'ADD', 'JMP', 'SUB', 'MUL',
    'DIV', 'MOD', 'JMZ', 'JMN', 'DJN', 'SPL',
    'CMP', 'SEQ', 'SNE', 'SLT', 'NOP'
]
list_of_modifiers = [
    '.AB', '.A', '.B', '.BA',
    '.F', '.X', '.I', None
]
list_of_modes = [
    '#', '$', '*', '@', '}',
    '{', '<', '>', None
]


class Read_from_file:
    def __init__(self, path) -> None:
        self.path = path
        self.lines = []
        try:
            with open(self.path, 'r') as file_handle:
                for line in file_handle:
                    self.line = line.rstrip().split()
                    self.lines.append(self.line)
        except FileNotFoundError:  # sprawzić
            return 'Wrong path'

    def get_mnemonic(self):
        mnemonic = self.line[0][:3]
        if mnemonic not in list_of_mnemonics:
            raise IncorrectMnemonicsError
        return mnemonic

    def get_modifier(self):
        modifier = self.line[0][3:]
        if len(modifier) == 0:
            modifier = None
        if modifier not in list_of_modifiers:
            raise IncorrectModifiersError
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
        if mode_1 not in list_of_modes:
            raise IncorrectOperandsError
        if type(value_1) != int:
            if value_1 is not None:
                raise IncorrectValueError
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
        if mode_2 not in list_of_modes:
            raise IncorrectOperandsError
        if type(value_2) != int:
            if value_2 is not None:
                raise IncorrectValueError
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
