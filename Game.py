from core_wars import (
    Core,
    Read_from_file,
    Warrior,
    Game
)


def main():

    instructions_1 = Read_from_file('wojownik_1.txt').get_instructions()
    warrior_1 = Warrior('Jakub', instructions_1, 19)

    instructions_2 = Read_from_file('wojownik_2.txt').get_instructions()
    warrior_2 = Warrior('Jaś', instructions_2, 5)

    instructions_3 = Read_from_file('wojownik_3.txt').get_instructions()
    warrior_3 = Warrior('Kuba', instructions_3, 3)

    instructions_4 = Read_from_file('wojownik_4.txt').get_instructions()
    warrior_4 = Warrior('Asia', instructions_4, 2)

    warriors = [warrior_1]

    core_1 = Core(10)

    game_1 = Game(core_1, warriors)

    game_1.prepare_game()

    core_1.visualize()

    game_1.play()

    core_1.visualize()


if __name__ == "__main__":
    main()
