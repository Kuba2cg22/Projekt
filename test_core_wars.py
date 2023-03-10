# +=''Dd""{}

from Errors import (
    IncorectPath,
    # NoWarriorInGame,
    # WrongPosition
)
from reader import Read_from_file

from core_wars import Core, Instruction, Warrior, Game, generate_instruction
from Visualize import visualize

import pytest


def test_create_warrior():
    global warrior_1
    warrior_1 = Warrior('Kuba', 10)


def test_create_file_with_wrong_path():
    global file_1
    with pytest.raises(IncorectPath):
        file_1 = Read_from_file('wojownik1.txt')


def test_create_file():
    global file_1
    file_1 = Read_from_file('wojownik_1.txt')


def test_warrior():
    instructions = []
    warrior_1 = Warrior('Kuba', instructions, 10)
    assert warrior_1.name == 'Kuba'
    assert warrior_1.instructions == []
    assert warrior_1.position == 10


def test_warrior_no_position():
    instructions = []
    warrior_1 = Warrior('Kuba', instructions)
    assert warrior_1.name == 'Kuba'
    assert warrior_1.instructions == []
    assert warrior_1.position == 0


def test_instruction():
    mnemonic = 'MOV'
    modifier = None
    operands = [[None, 3], ['#', 2]]
    comment = None
    instruction = Instruction([mnemonic, modifier, operands, comment])
    assert instruction.mnemonic() == 'MOV'
    assert instruction.modifier() is None
    assert instruction.operands() == [[None, 3], ['#', 2]]
    assert instruction.comment() is None


# def test_MOV():
#     global core_1, warriors
#     mnemonic = 'MOV'
#     modifier = None
#     operands = [[None, 0], ['#', 1]]
#     comment = None
#     instruction = Instruction([mnemonic, modifier, operands, comment])
#     instructions = [instruction]
#     core_1 = Core(
#         generate_instruction(10, ['DAT', None, [[None, 0], [None, 0]], None])
#         )
#     warrior_1 = Warrior('Kuba', instructions, 4)
#     warriors = [warrior_1]

# def test_list_of_instuctions():
#     file_1 = Read_from_file('wojownik_1.txt')
#     assert file_1.get_instructions() == [
#         ['ADD', None, [['#', '4'], [None, '3']], None],
#         ['MOV', None, [[None, '2'], ['@', '2']], None],
#         ['JMP', None, [[None, '-2'], [None, None]], None],
#         ['DAT', None, [['#', '0'], ['#', '4']], None]
#         ]


def test_create_core():
    global core_1
    core_1 = Core(
        generate_instruction(10, ['DAT', None, [[None, 0], [None, 0]], None])
        )


def test_size_core():
    core_1 = Core(
        generate_instruction(10, ['DAT', None, [[None, 0], [None, 0]], None])
        )
    assert len(core_1.memory) == 10


def test_memory_empty_core():
    core_1 = Core(
        generate_instruction(3, ['DAT', None, [[None, 0], [None, 0]], None])
        )
    assert len(core_1.memory) == 3
    assert list(visualize(core_1.memory)) == [
        (0, ['DAT', None, [[None, 0], [None, 0]], None]),
        (1, ['DAT', None, [[None, 0], [None, 0]], None]),
        (2, ['DAT', None, [[None, 0], [None, 0]], None])
        ]


def test_put_instruction_into_core():
    core_1 = Core(
        generate_instruction(3, ['DAT', None, [[None, 0], [None, 0]], None])
        )
    assert len(core_1.memory) == 3
    assert list(visualize(core_1.memory)) == [
        (0, ['DAT', None, [[None, 0], [None, 0]], None]),
        (1, ['DAT', None, [[None, 0], [None, 0]], None]),
        (2, ['DAT', None, [[None, 0], [None, 0]], None])
        ]
    mnemonic = 'MOV'
    modifier = None
    operands = [[None, 0], ['#', 1]]
    comment = None
    instruction = Instruction([mnemonic, modifier, operands, comment])
    core_1.put_instruction_into_core(1, instruction)
    assert list(visualize(core_1.memory)) == [
        (0, ['DAT', None, [[None, 0], [None, 0]], None]),
        (1, ['MOV', None, [[None, 0], ['#', 1]], None]),
        (2, ['DAT', None, [[None, 0], [None, 0]], None])
        ]


def test_execute_MOV_instruction_core():
    core_1 = Core(
        generate_instruction(3, ['DAT', None, [[None, 0], [None, 0]], None])
        )
    assert len(core_1.memory) == 3
    assert list(visualize(core_1.memory)) == [
        (0, ['DAT', None, [[None, 0], [None, 0]], None]),
        (1, ['DAT', None, [[None, 0], [None, 0]], None]),
        (2, ['DAT', None, [[None, 0], [None, 0]], None])
        ]
    mnemonic = 'MOV'
    modifier = None
    operands = [[None, 0], [None, 1]]
    comment = None
    instruction = Instruction([mnemonic, modifier, operands, comment])

    core_1.put_instruction_into_core(0, instruction)

    for position in range(3):
        core_1.execute_instruction(position)
    assert list(visualize(core_1.memory)) == [
        (0, ['MOV', None, [[None, 0], [None, 1]], None]),
        (1, ['MOV', None, [[None, 0], [None, 1]], None]),
        (2, ['MOV', None, [[None, 0], [None, 1]], None]),
        ]


def test_execute_MOV_AB_instruction_core():
    core_1 = Core(
        generate_instruction(3, ['DAT', None, [[None, 0], [None, 0]], None])
        )

    instructions = Read_from_file('wojownik_4.txt').get_instructions()
    warrior_4 = Warrior('Kuba', instructions, 0)

    game_1 = Game(core_1, [warrior_4])
    game_1.prepare_game()

    core_1.execute_instruction(warrior_4.get_position())

    assert list(visualize(core_1.memory)) == [
        (0, ['MOV', '.AB', [[None, 1], [None, 2]], None]),
        (1, ['ADD', None, [['#', 4], [None, 3]], None]),
        (2, ['MOV', None, [[None, 2], ['#', 4]], None]),
        ]


def test_execute_SPL_instruction_core():
    core_1 = Core(
        generate_instruction(5, ['DAT', None, [[None, 0], [None, 0]], None])
        )
    mnemonic = 'SPL'
    modifier = None
    operands = [[None, 1], [None, None]]
    comment = None
    instruction_1 = Instruction([mnemonic, modifier, operands, comment])

    mnemonic = 'MOV'
    modifier = None
    operands = [[None, 0], [None, 1]]
    comment = None
    instruction_2 = Instruction([mnemonic, modifier, operands, comment])

    core_1.put_instruction_into_core(0, instruction_1)
    core_1.put_instruction_into_core(1, instruction_2)

    core_1.execute_instruction(0)

    assert list(visualize(core_1.memory)) == [
        (0, ['SPL', None, [[None, 1], [None, None]], None]),
        (1, ['MOV', None, [[None, 0], [None, 1]], None]),
        (2, ['MOV', None, [[None, 0], [None, 1]], None]),
        (3, ['DAT', None, [[None, 0], [None, 0]], None]),
        (4, ['DAT', None, [[None, 0], [None, 0]], None])
        ]


def test_execute_warrior_1_instruction_core():
    core_1 = Core(
        generate_instruction(11, ['DAT', None, [[None, 0], [None, 0]], None])
        )

    instructions = Read_from_file('wojownik_1.txt').get_instructions()
    warrior_1 = Warrior('Kuba', instructions, 6)

    game_1 = Game(core_1, [warrior_1])
    game_1.prepare_game()

    game_1.play()

    assert list(visualize(core_1.memory)) == [
        (0, ['DAT', None, [[None, 0], [None, 0]], None]),
        (1, ['DAT', None, [[None, 0], [None, 0]], None]),
        (2, ['DAT', None, [['#', 0], ['#', 4]], None]),
        (3, ['DAT', None, [[None, 0], [None, 0]], None]),
        (4, ['DAT', None, [[None, 0], [None, 0]], None]),
        (5, ['DAT', None, [[None, 0], [None, 0]], None]),
        (6, ['DAT', None, [['#', 0], ['#', 8]], None]),
        (7, ['MOV', None, [[None, 2], ['@', 2]], None]),
        (8, ['JMP', None, [[None, -2], [None, None]], None]),
        (9, ['DAT', None, [['#', 0], ['#', 8]], None]),
        (10, ['DAT', None, [[None, 0], [None, 0]], None])
        ]

# def test_create_game():
#     warrior_1 = Warrior('wojownik_1.txt','Ja??', 3)
#     warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
#     warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
#     warriors = [warrior_1, warrior_2, warrior_3]
#     core_1 = Core(5)
#     game = Game(warriors, core_1)

# def test_game():
#     warrior_1 = Warrior('Ja??', 3)
#     warrior_2 = Warrior('Asia', 2)
#     warrior_3 = Warrior('Kuba', 1)
#     warriors = [warrior_1, warrior_2, warrior_3]
#     core_1 = Core(3)
#     game = Game(warriors, core_1)
#     assert game._warriors == [warrior_1, warrior_2, warrior_3]
#     assert game._core.memory == [
#         ['DAT', '', [None, None], [None, None], None],
#         ['DAT', '', [None, None], [None, None], None],
#         ['DAT', '', [None, None], [None, None], None]
#         ]


def test_create_empty_game():
    warriors = []
    core_1 = []
    game = Game(warriors, core_1)
    assert game._warriors == []
    assert game._core == []
