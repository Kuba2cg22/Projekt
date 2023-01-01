# +=''Dd""{}

from core_wars import Warrior, Game, IncorectPath, NoWarriorInGame
import pytest

def test_create_warrior():
    warrior_1 = Warrior('wojownik_1.txt')

def test_create_warrior_with_wrong_path():
    with pytest.raises(IncorectPath):
        warrior_1 = Warrior('wojownik1.txt')

def test_instuctions():
    warrior_1 = Warrior('wojownik_1.txt')
    assert warrior_1._list_of_instructions == [
        ['ADD', '#4', '3'],
        ['MOV', '2', '@2'],
        ['JMP', '-2'],
        ['DAT', '#0', '#4']
        ]

def test_create_game():
    warrior_1 = Warrior('wojownik_1.txt')
    warrior_2 = Warrior('wojownik_2.txt')
    warriors = [warrior_1, warrior_2]
    core_1 = []
    game = Game(warriors, core_1)

def test_game():
    warrior_1 = Warrior('wojownik_1.txt')
    warrior_2 = Warrior('wojownik_2.txt')
    warriors = [warrior_1, warrior_2]
    core_1 = [1432]
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1, warrior_2]
    assert game._core == [1432]

def test_create_empty_game():
    warriors = []
    core_1 = []
    game = Game(warriors, core_1)
    assert game._warriors == []
    assert game._core == []

def test_add_warrior_to_game():
    warrior_1 = Warrior('wojownik_1.txt')
    warrior_2 = Warrior('wojownik_2.txt')
    warriors = [warrior_1]
    core_1 = []
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1]
    game.add_warrior(warrior_2)
    assert game._warriors == [warrior_1, warrior_2]

def test_remove_warrior_from_game():
    warrior_1 = Warrior('wojownik_1.txt')
    warrior_2 = Warrior('wojownik_2.txt')
    warriors = [warrior_1, warrior_2]
    core_1 = []
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1, warrior_2]
    game.remove_warrior(warrior_2)
    assert game._warriors == [warrior_1]

def test_remove_not_present_warrior_from_game():
    warrior_1 = Warrior('wojownik_1.txt')
    warrior_2 = Warrior('wojownik_2.txt')
    warriors = [warrior_1]
    core_1 = []
    game = Game(warriors, core_1)
    assert game._warriors == [warrior_1]
    with pytest.raises(NoWarriorInGame):
        game.remove_warrior(warrior_2)
