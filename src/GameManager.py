from Pet import Pet
from pyfiglet import figlet_format as fig
from sys import exit
import csv
import webbrowser


class GameManager:
    version = '1.3.3'
    command_list = ['actions', 'sleep', 'pet', 'feed', 'stats', 'feelings',
                    'transfer', 'play', 'quit', 'manual (for more commands)']
    kinds = ['rock', 'fish', 'dog', 'cat', 'salad']
    safe_to_exit = False

    def __init__(self):
        self.start_up()
        self.pet = self.create_pet()
        self.choose_actions()  # Put tutorial in final prod

    def start_up(self):
        print('WELCOME TO')
        self.display_fig(f"CMD-PET (v{self.version})")
        print('by VukAnd and hellogoose.\n')

    def create_pet(self):
        print('welcome to the pet shop!')
        self.display_kinds()
        kind = self.get_user_input('which one would you like?')
        while kind not in self.kinds:
            print('we don\'t have that...')
            self.display_kinds()
            kind = self.get_user_input('please select one on the list.')
        name = self.get_user_input(
            'what would you like your new buddy to be named?'
        )
        player_pet = Pet(name, kind, self)

        self.display_fig(f"{player_pet.name} the {player_pet.kind}")
        print(f'this is {player_pet.name}, a {player_pet.kind}.')
        print('<( o  o )>')
        print('you need to take care of it.')
        print('type actions to see all the actions!')

        return player_pet

    def tutorial(self):
        self.actions_tutorial()

    def actions_tutorial(self):
        print('type actions to see all the actions!\n')
        while True:
            command = self.get_user_input()
            if command == 'actions':
                self.display_actions()
                self.choose_actions()
            else:
                print('a-c-t-i-o-n-s, type \'actions\'.')

    def choose_actions(self):
        """Allow user to enter commands via the '> '

        Note that the is_alive state of the pet can be switched to False during command = self.get_user_input(), thus, case of which has been considered.
        """
        while self.pet.is_alive:
            command = self.get_user_input()

            if self.pet.is_alive is not True:
                while command != "quit":
                    command = self.get_user_input('please type quit.')

                self.shut_down()

            if command == 'stats':
                self.pet.display_stats()
            elif command == 'sleep':
                self.pet.sleep()
            elif command == 'feed':
                self.pet.fed_bread()
            elif command == 'feed bread':
                self.pet.fed_bread()
            elif command == 'feed snack':
                self.pet.fed_snack()
            elif command == 'actions':
                self.display_actions()
            elif command == 'pet':
                self.pet.pet()
            elif command == 'feelings':
                self.pet.feelings()
            elif command == 'transfer':
                self.pet.transfer()
            elif command == 'manual':
                self.open_manual()
            elif command == 'play':
                self.pet.play_game1()
            elif command == 'quit':
                self.save_pet_data()
                self.shut_down()
            else:
                print(f"{self.pet.name} doesn\'t understand that command.")

            self.pet.display_complains()  # if any

        self.shut_down()

    def open_manual(self):
        confirmation = input(f'open manual in your browser? (y/n)')
        if confirmation == 'y':
            print('okay, opening now...')
            webbrowser.open(
                'https://github.com/cmdpet/cmd-pet/wiki', new=0, autoraise=True
            )

    def display_actions(self):
        print('actions include:')
        for command in self.command_list:
            print(" -- ", command)

    def display_kinds(self):
        print('the pet types include:')
        for kind in self.kinds:
            print(" -- ", kind)

    def get_user_input(self, text=None):
        """Get user input with the '> '.

        Returns:
        user_input -- str

        This function provides the clean UI and may perform surface-level amendments on the code. Should a filter be applied to ALL user inputs in the same fashion, that code should be added here.
        """
        if text is not None:
            print(text)
        user_input = input('> ')
        return user_input

    def display_fig(self, text: str):
        """Display a large text figure.

        Keyword arguments:
        text -- str

        Using the pyfiglet module, the text string is transformed into a large text figure and is then printed.
        """
        logo = fig(text)
        print(logo)

    def save_pet_data(self):
        self.pet.is_alive = False  # Tells pet's data to stop changing
        self.pet.main_thread.join()  # Waits for pet to stop before saving data
        info_to_save = []
        info_to_save.append(self.pet.name)
        info_to_save.append(self.pet.kind)
        info_to_save.append(self.pet.time_in_loop)  # Given once the thread ends
        for key in self.pet.stats:  # The order matters, see Pet.raw_stats
            info_to_save.append(self.pet.stats[key]["val"])
        with open('cmdpet_save.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(info_to_save)

    def shut_down(self):
        """Exits the interpreter."""
        print("closing application...")
        exit()
