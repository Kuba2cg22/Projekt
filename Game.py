from core_wars import (
    Core,
    Read_from_file,
    Warrior,
    Game
)


def main():

    instructions_1 = Read_from_file('wojownik_1.txt').get_instructions()
    warrior_1 = Warrior('Jakub', instructions_1, 3)

    instructions_2 = Read_from_file('wojownik_2.txt').get_instructions()
    warrior_2 = Warrior('Jaś', instructions_2, 10)

    instructions_3 = Read_from_file('wojownik_3.txt').get_instructions()
    warrior_3 = Warrior('Kuba', instructions_3, 3)

    instructions_4 = Read_from_file('wojownik_4.txt').get_instructions()
    warrior_4 = Warrior('Asia', instructions_4, 2)

    warriors = [warrior_4]

    core_1 = Core(16)

    game_1 = Game(core_1, warriors)

    game_1.prepare_game()

    core_memory_1 = core_1.visualize()

    for register in core_memory_1:
        print(register)

    game_1.play()

    core_memory_2 = core_1.visualize()

    for register in core_memory_2:
        print(register)


if __name__ == "__main__":
    main()
