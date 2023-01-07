# +=''Dd""{}

from core_wars import Core, Instruction, Operand, Warrior, Game, IncorectPath, NoWarriorInGame, WrongPosition
import pytest


def test_create_warrior():
    warrior_1 = Warrior('wojownik_1.txt', 'Kuba', 10)

def test_create_warrior_with_wrong_path():
    with pytest.raises(IncorectPath):
        warrior_1 = Warrior('wojownik1.txt', 'Kuba', 10)
        warrior_1.instructions()

def test_warrior():
    warrior_1 = Warrior('wojownik_1.txt', 'Kuba', 10)
    assert warrior_1.path == 'wojownik_1.txt'
    assert warrior_1.name == 'Kuba'
    assert warrior_1.position == 10

def test_warrior_no_position():
    warrior_1 = Warrior('wojownik_1.txt', 'Kuba')
    assert warrior_1.path == 'wojownik_1.txt'
    assert warrior_1.name == 'Kuba'
    assert warrior_1.position == 0

def test_list_of_instuctions():
    warrior_1 = Warrior('wojownik_1.txt', 'Kuba', 10)
    assert warrior_1.instructions() == [
        ['ADD', '', ['#', '4'], [None, '3'], None],
        ['MOV', '', [None, '2'], ['@', '2'], None],
        ['JMP', '', [None, '-2'], [None, None], None],
        ['DAT', '', ['#', '0'], ['#', '4'], None]
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
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None]
        ]

def test_put_instruction_into_core():
    core_1 = Core(3)
    assert core_1.size == 3
    assert core_1.memory == [
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None]
        ]
    core_1.put_instruction_into_core(['MOV', '', [None, '0'], [None, '1'], None], 1)
    assert core_1.memory == [
        ['NOP', '', [None, None], [None, None], None],
        ['MOV', '', [None, '0'], [None, '1'], None],
        ['NOP', '', [None, None], [None, None], None]
        ]

def test_execute_MOV_instruction_core():
    core_1 = Core(3)
    assert core_1.size == 3
    assert core_1.memory == [
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None]
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
    warrior_1 = Warrior('wojownik_1.txt','Jaś', 3)
    warrior_2 = Warrior('wojownik_2.txt','Asia', 2)
    warrior_3 = Warrior('wojownik_3.txt','Kuba', 1)
    warriors = [warrior_1, warrior_2, warrior_3]
    core_1 = Core(3)
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1, warrior_2, warrior_3]
    assert game._core.memory == [
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None],
        ['NOP', '', [None, None], [None, None], None]
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
