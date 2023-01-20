from core_wars import (
    Core,
    Warrior,
    Game,
    generate_instruction
)

# from matplotlib import animation

from reader import Read_from_file


def main():

    instructions_1 = Read_from_file('wojownik_1.txt').get_instructions()
    warrior_1 = Warrior('Jakub', instructions_1, 6)

    instructions_2 = Read_from_file('wojownik_2.txt').get_instructions()
    warrior_2 = Warrior('Jaś', instructions_2, 4)

    # instructions_3 = Read_from_file('wojownik_3.txt').get_instructions()
    # warrior_3 = Warrior('Kuba', instructions_3, 3)

    instructions_4 = Read_from_file('wojownik_4.txt').get_instructions()
    warrior_4 = Warrior('Asia', instructions_4, 2)

    warriors = [warrior_4, warrior_1]

    core_1 = Core(
        generate_instruction(10, ['DAT', None, [[None, 0], [None, 0]], None])
        )

    game_1 = Game(core_1, warriors)

    game_1.prepare_game()

    print('Ready core: ')
    core_memory_1 = core_1.visualize()

    for register in core_memory_1:
        print(register)

    game_1.play()

    core_memory_2 = core_1.visualize()

    for register in core_memory_2:
        print(register)


if __name__ == "__main__":
    main()
