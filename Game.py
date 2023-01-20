from core_wars import (
    Core,
    Warrior,
    Game,
    generate_instruction
)

# from matplotlib import animation

from reader import Read_from_file

from Visualize import visualize


def main():

    print('STARTING CORE WARS GAME!\n')

    instructions_1 = Read_from_file('wojownik_1.txt').get_instructions()
    warrior_1 = Warrior('Jakub', instructions_1, 6)

    # instructions_2 = Read_from_file('wojownik_2.txt').get_instructions()
    # warrior_2 = Warrior('Jaś', instructions_2, 4)

    # instructions_3 = Read_from_file('wojownik_3.txt').get_instructions()
    # warrior_3 = Warrior('Kuba', instructions_3, 3)

    # instructions_4 = Read_from_file('wojownik_4.txt').get_instructions()
    # warrior_4 = Warrior('Asia', instructions_4, 2)

    warriors = [warrior_1]

    core_size = input('Choose the size of the core: \n')
    core_1 = Core(
        generate_instruction(
            int(core_size), ['DAT', None, [[None, 0], [None, 0]], None]
            )
        )

    game_1 = Game(core_1, warriors)

    game_1.prepare_game()

    print('Core is ready to execute instructions. \n')
    answer = input('Do you want to see the memory of the core?(y/n)\n')
    if answer.upper() == 'Y':
        for register in list(visualize(core_1.memory)):
            print(register)
    start = input('Do you want to start the game?(y/n)\n')
    if start.upper() == 'Y':
        game_1.play()

    print('Game has ended. \n')
    answer = input('Do you want to see the memory of the core?(y/n)\n')
    if answer.upper() == 'Y':
        for register in list(visualize(core_1.memory)):
            print(register)


if __name__ == "__main__":
    main()
