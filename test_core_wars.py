# +=''Dd""{}

from core_wars import Core, Instruction, Read_from_file, Warrior, Game, IncorectPath, NoWarriorInGame, WrongPosition
import pytest


def test_create_warrior():
    warrior_1 = Warrior('Kuba', 10)


def test_create_file_with_wrong_path():
    with pytest.raises(IncorectPath):
        file_1 = Read_from_file('wojownik1.txt')


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


def test_instuction():
    mnemonic = 'MOV'
    modifier = None
    operands = [[None, '3'], ['#', 2]]
    comment = None
    instruction = Instruction([mnemonic, modifier, operands, comment])
    assert instruction.mnemonic == 'MOV'


def test_list_of_instuctions():
    file_1 = Read_from_file('wojownik_1.txt')
    assert file_1.get_instructions() == [
        ['ADD', None, [['#', '4'], [None, '3']], None],
        ['MOV', None, [[None, '2'], ['@', '2']], None],
        ['JMP', None, [[None, '-2'], [None, None]], None],
        ['DAT', None, [['#', '0'], ['#', '4']], None]
        ]


def test_create_core():
    core_1 = Core(10)


def test_size_core():
    core_1 = Core(10)
    assert core_1.size == 10


def test_memory_empty_core():
    core_1 = Core(3)
    assert core_1.size == 3
    assert core_1.memory == [
        ['DAT', None, [[None, None], [None, None]], None],
        ['DAT', None, [[None, None], [None, None]], None],
        ['DAT', None, [[None, None], [None, None]], None]
        ]

def test_put_instruction_into_core():
    core_1 = Core(3)
    assert core_1.size == 3
    assert core_1.memory == [
        ['DAT', None, [[None, None], [None, None]], None],
        ['DAT', None, [[None, None], [None, None]], None],
        ['DAT', None, [[None, None], [None, None]], None]
        ]
    core_1.put_instruction_into_core(
        1, ['MOV', None, [[None, '0'], [None, '1']], None]
        )
    assert core_1.memory == [
        ['DAT', None, [[None, None], [None, None]], None],
        ['MOV', None, [[None, '0'], [None, '1']], None],
        ['DAT', None, [[None, None], [None, None]], None]
        ]

def test_execute_MOV_instruction_core():
    core_1 = Core(3)
    assert core_1.size == 3
    assert core_1.memory == [
        ['DAT', '', [None, None], [None, None], None],
        ['DAT', '', [None, None], [None, None], None],
        ['DAT', '', [None, None], [None, None], None]
        ]
    core_1.put_instruction_into_core(['MOV', '', [None, '0'], [None, '1'], None], 1)
    core_1.execute_instructions()
    assert core_1.memory == [
        ['MOV', '', [None, '0'], [None, '1'], None],
        ['MOV', '', [None, '0'], [None, '1'], None],
        ['MOV', '', [None, '0'], [None, '1'], None]
        ]



def test_create_game():
    warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
    warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
    warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
    warriors = [warrior_1, warrior_2, warrior_3]
    core_1 = Core(5)
    game = Game(warriors, core_1)

def test_game():
    warrior_1 = Warrior('Jaś', 3)
    warrior_2 = Warrior('Asia', 2)
    warrior_3 = Warrior('Kuba', 1)
    warriors = [warrior_1, warrior_2, warrior_3]
    core_1 = Core(3)
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1, warrior_2, warrior_3]
    assert game._core.memory == [
        ['DAT', '', [None, None], [None, None], None],
        ['DAT', '', [None, None], [None, None], None],
        ['DAT', '', [None, None], [None, None], None]
        ]

def test_create_empty_game():
    warriors = []
    core_1 = []
    game = Game(warriors, core_1)
    assert game._warriors == []
    assert game._core == []

def test_add_warrior_to_game():
    warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
    warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
    warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
    warriors = [warrior_1]
    core_1 = Core(4)
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1]
    game.add_warrior(warrior_2)
    assert game._warriors == [warrior_1, warrior_2]

def test_remove_warrior_from_game():
    warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
    warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
    warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
    warriors = [warrior_1, warrior_2]
    core_1 = Core(5)
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1, warrior_2]
    game.remove_warrior(warrior_2)
    assert game._warriors == [warrior_1]

def test_remove_not_present_warrior_from_game():
    warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
    warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
    warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
    warriors = [warrior_1]
    core_1 = Core(5)
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1]
    with pytest.raises(NoWarriorInGame):
        game.remove_warrior(warrior_2)
