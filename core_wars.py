# +=''dD""{}

import copy


from Errors import (
    NoWarriorInGame,
    IncorrectModifiersError,
    IncorrectOperandsError
    )


SplitProces = False
game_result = 'undecided'


def generate_instruction(size, instruction):
    '''
    generates different objects of instruction with the same parameters
    '''
    for i in range(size):
        yield Instruction(instruction)


class Core:
    '''
    Initialize the core
    '''
    def __init__(self, instructions):
        self.memory = []
        for instruction in instructions:
            self.memory.append(instruction)
        self.size = len(self.memory)

    def get_size(self):
        return self.size

    def get_memory(self):
        return self.memory

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
        global SplitProces
        self.set_position(position)
        instruction = self.memory[position]
        mnemonic = instruction.mnemonic()
        method = mnemonics[mnemonic](instruction, position, self)
        method.run()

        if SplitProces:
            self.execute_instruction(self.position)


class Instruction:
    '''
    Enables access to the parts of single instruction
    '''
    def __init__(self, instruction):
        self.instruction = instruction

    def mnemonic(self):
        return self.instruction[0]

    def modifier(self):
        return self.instruction[1]

    def operands(self):
        return self.instruction[2]

    def operands_A(self):
        return self.instruction[2][0]

    def set_operands_A(self, new_operands_A):
        self.instruction[2][0] = new_operands_A

    def operands_B(self):
        return self.instruction[2][1]

    def set_operands_B(self, new_operands_B):
        self.instruction[2][1] = new_operands_B

    def mode_1(self):
        return self.instruction[2][0][0]

    def value_1(self):
        return self.instruction[2][0][1]

    def set_value_1(self, new_value):
        self.instruction[2][0][1] = new_value

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


class DAT(Instruction):
    '''
    data (kills the process)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False
        global game_result
        game_result = 'lost'


class MOV(Instruction):
    '''
    move (copies data from one address to another)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        instruction_to_copy = self.core.memory[source_index]
        copy_of_instuction = copy.deepcopy(instruction_to_copy)

        destination_index = calculate_destination_index(self)

        if self.instruction.modifier() == '.AB':
            self.core.memory[destination_index].set_operands_B(
                instruction_to_copy.operands_A()
            )
        elif self.instruction.modifier() == '.A':
            self.core.memory[destination_index].set_operands_A(
                instruction_to_copy.operands_A()
            )
        elif self.instruction.modifier() == '.B':
            self.core.memory[destination_index].set_operands_B(
                instruction_to_copy.operands_B()
            )
        elif self.instruction.modifier() == '.BA':
            self.core.memory[destination_index].set_operands_A(
                instruction_to_copy.operands_B()
            )
        elif self.instruction.modifier() == '.F':
            self.core.memory[destination_index].set_operands_A(
                instruction_to_copy.operands_A()
            )
            self.core.memory[destination_index].set_operands_B(
                instruction_to_copy.operands_B()
            )
        elif self.instruction.modifier() == '.X':
            self.core.memory[destination_index].set_operands_A(
                instruction_to_copy.operands_B()
            )
            self.core.memory[destination_index].set_operands_B(
                instruction_to_copy.operands_A()
            )
        else:
            self.core.memory[destination_index] = copy_of_instuction

            if self.instruction.operands()[1][0] == '}':
                self.core.memory[destination_index].set_value_1(
                    self.core.memory[destination_index].operands()[0][1]
                    + self.instruction.operands()[1][1]
                )

            elif self.instruction.operands()[1][0] == '>':
                self.core.memory[destination_index].set_value_2(
                    self.core.memory[destination_index].operands()[1][1]
                    + self.instruction.operands()[1][1]
                )

        self.core.next_position()


class ADD(Instruction):
    '''
    add (adds one number to another)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        source_instruction = self.core.memory[source_index]
        destination_index = calculate_destination_index(self)
        instruction_to_change = self.core.memory[destination_index]

        wrong_modifiers = ['.F', '.X']
        if self.instruction.modifier() in wrong_modifiers:
            raise IncorrectModifiersError

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                new_value = source_instruction.operands()[0][1] +\
                    instruction_to_change.operands()[1][1]
            elif self.instruction.modifier() == '.A':
                new_value = source_instruction.operands()[0][1] +\
                    instruction_to_change.operands()[0][1]
            elif self.instruction.modifier() == '.BA':
                new_value = source_instruction.operands()[1][1] +\
                    instruction_to_change.operands()[0][1]
            elif self.instruction.modifier() == '.A':
                new_value = source_instruction.operands()[0][1] +\
                    instruction_to_change.operands()[0][1]
            else:
                new_value = self.instruction.operands()[0][1] +\
                    instruction_to_change.operands()[1][1]

        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                new_value = source_instruction.operands()[1][1] +\
                    instruction_to_change.operands()[1][1]

        else:
            raise IncorrectOperandsError

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class JMP(Instruction):
    '''
    jump (continues execution from another address)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        if self.instruction.operands_B() != [None, None]:
            raise IncorrectOperandsError
        global SplitProces
        SplitProces = False
        new_position = self.instruction.operands()[0][1] + self.position
        self.core.set_position(new_position)


class JMZ(Instruction):
    '''
    jump if zero (tests a number and jumps to an address if it's 0)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        if self.instruction.operands_B() != [None, None]:
            raise IncorrectOperandsError
        global SplitProces
        SplitProces = False

        new_position = self.instruction.operands()[0][1] + self.position
        if new_position == 0:
            self.core.set_position(new_position)
        else:
            self.core.set_position(new_position)


class JMN(Instruction):
    '''
    jump if not zero (tests a number and jumps if it isn't 0)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        if self.instruction.operands_B() != [None, None]:
            raise IncorrectOperandsError
        global SplitProces
        SplitProces = False

        new_position = self.instruction.operands()[0][1] + self.position
        if new_position != 0:
            self.core.set_position(new_position)
        else:
            self.core.set_position(new_position)


class DJN(Instruction):
    '''
    decrement and jump if not zero
    (decrements a number by one, and jumps unless the result is 0)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        if self.instruction.operands_B() != [None, None]:
            raise IncorrectOperandsError
        new_position = self.instruction.operands()[0][1] + self.position - 1
        if new_position != 0:
            self.core.set_position(new_position)
        else:
            self.core.set_position(new_position)


class SUB(Instruction):
    '''
    subtract (subtracts one number from another)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        source_instruction = self.core.memory[source_index]
        destination_index = calculate_destination_index(self)
        instruction_to_change = self.core.memory[destination_index]

        wrong_modifiers = ['.F', '.X']
        if self.instruction.modifier() in wrong_modifiers:
            raise IncorrectModifiersError

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                new_value = instruction_to_change.operands()[1][1] -\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] -\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.BA':
                new_value = instruction_to_change.operands()[0][1] -\
                    source_instruction.operands()[1][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] -\
                    source_instruction.operands()[0][1]
            else:
                new_value = instruction_to_change.operands()[1][1] -\
                    instruction_to_change.operands()[0][1]

        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                new_value = instruction_to_change.operands()[1][1] -\
                    source_instruction.operands()[1][1]

        else:
            raise IncorrectOperandsError

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class NOP(Instruction):
    '''
    no operation (does nothing)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        self.core.next_position()


class MUL(Instruction):
    '''
    multiply (multiplies one number with another)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        source_instruction = self.core.memory[source_index]
        destination_index = calculate_destination_index(self)
        instruction_to_change = self.core.memory[destination_index]

        wrong_modifiers = ['.F', '.X']
        if self.instruction.modifier() in wrong_modifiers:
            raise IncorrectModifiersError

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                new_value = instruction_to_change.operands()[1][1] *\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] *\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.BA':
                new_value = instruction_to_change.operands()[0][1] *\
                    source_instruction.operands()[1][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] *\
                    source_instruction.operands()[0][1]
            else:
                new_value = instruction_to_change.operands()[1][1] *\
                    instruction_to_change.operands()[0][1]

        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                new_value = instruction_to_change.operands()[1][1] *\
                    source_instruction.operands()[1][1]

        else:
            raise IncorrectOperandsError

        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class DIV(Instruction):
    '''
    divide (divides one number with another)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        source_instruction = self.core.memory[source_index]
        destination_index = calculate_destination_index(self)
        instruction_to_change = self.core.memory[destination_index]

        wrong_modifiers = ['.F', '.X']
        if self.instruction.modifier() in wrong_modifiers:
            raise IncorrectModifiersError

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                new_value = instruction_to_change.operands()[1][1] //\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] //\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.BA':
                new_value = instruction_to_change.operands()[0][1] //\
                    source_instruction.operands()[1][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] //\
                    source_instruction.operands()[0][1]
            else:
                new_value = instruction_to_change.operands()[1][1] //\
                    instruction_to_change.operands()[0][1]

        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                new_value = instruction_to_change.operands()[1][1] //\
                    source_instruction.operands()[1][1]

        else:
            raise IncorrectOperandsError
        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class MOD(Instruction):
    '''
    modulus (divides one number with another and gives the remainder)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]

        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()

        source_instruction = self.core.memory[source_index]
        destination_index = calculate_destination_index(self)
        instruction_to_change = self.core.memory[destination_index]

        wrong_modifiers = ['.F', '.X']
        if self.instruction.modifier() in wrong_modifiers:
            raise IncorrectModifiersError

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                new_value = instruction_to_change.operands()[1][1] %\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] %\
                    source_instruction.operands()[0][1]
            elif self.instruction.modifier() == '.BA':
                new_value = instruction_to_change.operands()[0][1] %\
                    source_instruction.operands()[1][1]
            elif self.instruction.modifier() == '.A':
                new_value = instruction_to_change.operands()[0][1] %\
                    source_instruction.operands()[0][1]
            else:
                new_value = instruction_to_change.operands()[1][1] %\
                    instruction_to_change.operands()[0][1]

        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                new_value = instruction_to_change.operands()[1][1] %\
                    source_instruction.operands()[1][1]

        else:
            raise IncorrectOperandsError
        modes_to_A_field = ['*', '{', '}']
        modes_to_B_field = ['@', '<', '>', None]

        if self.instruction.operands()[1][0] in modes_to_A_field:
            instruction_to_change.set_value_1(new_value)

        elif self.instruction.operands()[1][0] in modes_to_B_field:
            instruction_to_change.set_value_2(new_value)

        self.core.next_position()


class SPL(Instruction):
    '''
    split (starts a second process at another address)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        if self.instruction.operands_B() != [None, None]:
            raise IncorrectOperandsError
        new_position = self.instruction.operands()[0][1] + self.position
        self.core.set_position(new_position)
        global SplitProces
        SplitProces = True


class CMP(Instruction):
    '''
    compare (same as SEQ)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]
        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()
        destination_index = calculate_destination_index(self)

        instruction_1 = self.core.memory[source_index]
        instruction_2 = self.core.memory[destination_index]

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                value_1 = self.instruction.operands()[0][1]
                value_2 = instruction_2.operands()[1][1]
                if value_1 == value_2:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                value_1 = self.instruction.operands()[1][1]
                value_2 = instruction_2.operands()[1][1]
                if value_1 == value_2:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        elif self.instruction.operands()[1][0] is None and self.instruction.operands()[0][0] is None:
            if self.instruction.modifier() == '.I':
                is_mnemonics = bool(instruction_1.mnemonic() == instruction_2.mnemonic())
                is_modifiers = bool(instruction_1.modifier() == instruction_2.modifier())
                is_operands = bool(instruction_1.operands() == instruction_2.operands())
                is_comments = bool(instruction_1.comment() == instruction_2.comment())

                if is_mnemonics and is_modifiers and is_operands and is_comments:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        else:
            raise IncorrectOperandsError

        self.core.next_position()


class SEQ(Instruction):
    '''
    skip if equal(compares two instructions,
     and skips the next instruction if they are equal)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]
        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()
        destination_index = calculate_destination_index(self)

        instruction_1 = self.core.memory[source_index]
        instruction_2 = self.core.memory[destination_index]

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                value_1 = self.instruction.operands()[0][1]
                value_2 = instruction_2.operands()[1][1]
                if value_1 == value_2:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                value_1 = self.instruction.operands()[1][1]
                value_2 = instruction_2.operands()[1][1]
                if value_1 == value_2:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        elif self.instruction.operands()[1][0] is None and self.instruction.operands()[0][0] is None:
            if self.instruction.modifier() == '.I':
                is_mnemonics = bool(instruction_1.mnemonic() == instruction_2.mnemonic())
                is_modifiers = bool(instruction_1.modifier() == instruction_2.modifier())
                is_operands = bool(instruction_1.operands() == instruction_2.operands())
                is_comments = bool(instruction_1.comment() == instruction_2.comment())

                if is_mnemonics and is_modifiers and is_operands and is_comments:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        else:
            raise IncorrectOperandsError

        self.core.next_position()


class SNE(Instruction):
    '''
    skip if not equal (compares two instructions,
    and skips the next instruction if they aren't equal)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        source_index = self.position + self.instruction.operands()[0][1]
        while source_index >= self.core.get_size():
            source_index -= self.core.get_size()
        destination_index = calculate_destination_index(self)

        instruction_1 = self.core.memory[source_index]
        instruction_2 = self.core.memory[destination_index]

        if self.instruction.operands()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                value_1 = self.instruction.operands()[0][1]
                value_2 = instruction_2.operands()[1][1]
                if value_1 != value_2:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        elif self.instruction.operands()[1][0] == '#' and self.instruction.operands()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                value_1 = self.instruction.operands()[1][1]
                value_2 = instruction_2.operands()[1][1]
                if value_1 != value_2:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        elif self.instruction.operands()[1][0] is None and self.instruction.operands()[0][0] is None:
            if self.instruction.modifier() == '.I':
                is_mnemonics = bool(instruction_1.mnemonic() != instruction_2.mnemonic())
                is_modifiers = bool(instruction_1.modifier() != instruction_2.modifier())
                is_operands = bool(instruction_1.operands() != instruction_2.operands())
                is_comments = bool(instruction_1.comment() != instruction_2.comment())

                if is_mnemonics and is_modifiers and is_operands and is_comments:
                    self.core.set_position(self.position + 1)
            else:
                raise IncorrectModifiersError
        else:
            raise IncorrectOperandsError

        self.core.next_position()


class SLT(Instruction):
    '''
    skip if lower than (compares two values, and skips the next instruction
    if the first is lower than the second)
    '''
    def __init__(self, instruction, position, core):
        super().__init__(instruction)
        self.position = position
        self.core = core

    def run(self):
        global SplitProces
        SplitProces = False

        wrong_modifiers = ['.F', '.X', '.A', '.I']
        if self.instruction.modifier() in wrong_modifiers:
            raise IncorrectModifiersError

        if self.instruction.openends()[0][0] == '#':
            if self.instruction.modifier() == '.AB':
                value_1 = self.instruction.operands()[0][1]
                value_2 = self.instruction.operands()[1][1]
            else:
                raise IncorrectModifiersError
        elif self.instruction.openends()[0][0] != '#':
            if self.instruction.modifier() == '.B':
                source_index = self.position + self.instruction.operands()[0][1]

                while source_index >= self.core.get_size():
                    source_index -= self.core.get_size()

                source_instruction = self.core.memory[source_index]

                destination_index = calculate_destination_index(self)

                destination_instruction = self.core.memory[destination_index]

                value_1 = source_instruction.operands()[1][1]
                value_2 = destination_instruction.operands()[1][1]
            else:
                raise IncorrectModifiersError
        else:
            raise IncorrectOperandsError

        if value_1 < value_2:
            self.core.set_position(self.position + 1)

        self.core.next_position()


def calculate_destination_index(self):
    '''
    calculates the destination index according to addressing modes
    '''
    pointed_index = self.position + self.instruction.operands()[1][1]

    while pointed_index >= self.core.get_size():
        pointed_index -= self.core.get_size()

    pointed_instruction = self.core.memory[pointed_index]

    if self.instruction.operands()[1][0] is None:

        destination_index = self.position + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '*':
        destination_index = self.position + pointed_instruction.operands()[0][1]\
            + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '@':
        destination_index = self.position + pointed_instruction.operands()[1][1]\
            + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '<':

        destination_index = self.position + pointed_instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '>':

        destination_index = self.position + pointed_instruction.operands()[1][1]\
                + self.instruction.operands()[1][1]

    elif self.instruction.operands()[1][0] == '{':

        destination_index = self.position + pointed_instruction.operands()[0][1]

    elif self.instruction.operands()[1][0] == '}':

        destination_index = self.position + pointed_instruction.operands()[0][1]\
                + self.instruction.operands()[1][1]
    else:
        destination_index = self.position + self.instruction.operands()[1][1]

    while destination_index >= self.core.get_size():
        destination_index -= self.core.get_size()

    return destination_index


mnemonics = {
    'DAT': DAT,
    'MOV': MOV,
    'ADD': ADD,
    'JMP': JMP,
    'SUB': SUB,
    'MUL': MUL,
    'DIV': DIV,
    'MOD': MOD,
    'JMZ': JMZ,
    'JMN': JMN,
    'DJN': DJN,
    'SPL': SPL,
    'CMP': CMP,
    'SEQ': SEQ,
    'SNE': SNE,
    'SLT': SLT,
    'NOP': NOP
}


class Warrior:
    '''
    Initialize warrior with given name, instructions and strating position
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

    def next_position(self):
        self.position += 1
        return self.position


class Game:
    '''
    Initialize whole core wars game
    '''
    def __init__(self, core, warriors) -> None:
        self._warriors = warriors if warriors else []
        self._core = core if core else []

    def prepare_game(self):
        '''
        prepares core to be ready to execute instructions
        '''
        for warrior in self._warriors:

            while warrior.position not in range(self._core.size):
                new_position = warrior.position - self._core.size
                warrior.start_position = warrior.set_position(new_position)

            position = warrior.position

            for instruction in warrior.instructions:
                self._core.put_instruction_into_core(position, instruction)
                position += 1
                if position == self._core.size:
                    position = warrior.set_position(0)

    def play(self):
        '''
        starts the game
        '''
        round = 1
        global game_result
        while game_result == 'undecided':
            print(f'Round: {round}')
            if self._warriors:
                for warrior in self._warriors:
                    print(f'Warrior: {warrior.get_name()}')
                    position = warrior.position
                    if position == self._core.size:
                        position = warrior.set_position(0)
                    self._core.execute_instruction(position)
                    warrior.set_position(self._core.get_position())
                    if round > 100:
                        answer = input('Round is over 100. Proceed?(y/n)')
                        if answer == 'y':
                            continue
                        else:
                            game_result = 'drew'
            else:
                raise NoWarriorInGame
            round += 1
        print(f'Game result: Warrior {warrior.get_name()} {game_result}.')
