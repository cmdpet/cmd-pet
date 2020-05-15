import time
from random import randrange
from collections import defaultdict
from threading import Thread, Event
from random import choices
from tqdm import tqdm


class Pet:
    raw_stats = {('energy', 'val'): 0,  # to be worked on
                 ('energy', 'max'): 100,
                 ('happiness', 'val'): 0,
                 ('happiness', 'max'): 100,
                 ('hunger', 'val'): 0,
                 ('hunger', 'max'): 100,
                 ('snack meter', 'val'): 1,
                 ('snack meter', 'min'): 1}

    stop_threads = False
    is_alive = True
    lifetime = 0

    def __init__(self, name, kind, game_manager):
        self.name = name
        self.kind = kind

        # transforms the data in raw_stats into a nested dictionary
        self.stats = defaultdict(dict)
        for (attribute, detail), val in self.raw_stats.items():
            self.stats[attribute][detail] = val

        # assigns initial values for stats into nested dictionary with
        # randomized values
        self.stats["energy"]["val"] = randrange(50, 90)
        self.stats["happiness"]["val"] = randrange(50, 90)
        self.stats["hunger"]["val"] = randrange(50, 90)

        self.main_thread = Thread(
            target=self.decrease_stats
        )
        self.main_thread.setDaemon(True)
        self.main_thread.start()

        self.game_manager = game_manager

    def decrease_stats(self):
        """Decreases stat values every 60 seconds.

        Whilst the is_alive state of the pet is True, all of the stats of the pet will decrease, either randomly or with a set value, after every 60 seconds. The lifetime is also recorded in minutes. After each change, all values will be evaluated with the check_if_dead() method to ensure that the pet is indeed still alive. Since this thread is daemonic, it will close itself once the sys.exit() is called.
        """

        frequency = 60  # how many seconds until stat change is in effect.
        last_change = time.time()
        while self.is_alive:
            if (time.time() - last_change) > frequency:
                last_change = time.time()
                self.lifetime += 1  # in minutes
                for attr in self.stats:
                    if attr == 'snack meter':
                        self.add_to_stat(attr, -1, False)
                    else:
                        self.add_to_stat(attr, (-1 * randrange(30)), False)

                self.check_if_dead()
        else:
            self.time_in_loop = time.time() - last_change

    def check_if_dead(self):
        if self.stats['energy']['val'] < 0:
            print(f'{self.name} has died due to being too tired. :(')
            self.end()
        elif self.stats['hunger']['val'] < 0:
            print(f'{self.name} has died due to hunger. :(')
            self.end()
        elif self.stats['happiness']['val'] < 0:
            print(f'{self.name} has died due to sadness. :(')
            self.end()
        elif self.stats['snack meter']['val'] > 5:
            print(f'{self.name} has died from severe overeating. :(')
            self.end()

    def display_complains(self):
        complains = []

        if self.stats['energy']['val'] < 50:
            complains.append('<(-  -)> i\'m tired')
        if self.stats['hunger']['val'] < 50:
            complains.append('<(o  O  o)> i\'m hungry')
        if self.stats['happiness']['val'] < 50:
            complains.append('<(T  T)> i\'m sad')

        if len(complains) != 0:  # if there are complains
            text = choices(complains)[0]

            print('\n' + text)  # to recreate the user input UI

    def display_stats(self):
        for key, val in self.stats.items():
            # val = {'max': ..., 'val': ...}, or without the 'max'
            if 'max' in val:
                print(key + ": " + str(val['val']) + "/" + str(val['max']))
            else:
                print(key + ": " + str(val['val']))

    def sleep(self):
        print(f'<(  u _ u )>\n{self.name} is sleeping...')
        self.sleep_animation()
        print(f'<( o  o )>\n{self.name} is awake!')
        self.add_to_stat("energy", 30)

    def sleep_animation(self):
        sleepy_time = randrange(60)
        for i in tqdm(range(sleepy_time), desc='ZZZ'):
                time.sleep(0.25)

    def fed_bread(self):
        print('    bread\n    ^  ^\n( o  o )')
        eat_time = randrange(10)
        for i in tqdm(range(eat_time), desc='Eating'):
                time.sleep(0.25)
        print('<( o <ead> o )>\nyummy!')
        self.add_to_stat("hunger", randrange(15))

    def fed_snack(self):
        print('    snack\n    ^  ^\n( o  o )')
        eat_time = randrange(10)
        for i in tqdm(range(eat_time), desc='Eating'):
                time.sleep(0.25)
        print('<( o <ead> o )>\nyummy!')
        self.add_to_stat("hunger", randrange(15))
        self.add_to_stat("snack meter", 1)
        self.add_to_stat("happiness", randrange(10))

    def pet(self):
        print('^( o  o )>')
        time.sleep(0.5)
        print('<( o  o )^')
        self.add_to_stat("happiness", randrange(10))

    def feelings(self):
        """Displays the feelings of the pet.

        If the pet does not meet the threshold, then the display_complain will display the pet's complains instead.
        """
        threshold = self.stats['happiness']['max'] / 2
        if self.stats['happiness']['val'] >= threshold:
            print('<( ^ ^ )>\ni am very happy!')

    def transfer(self):
        print(f'Are you sure you want to transfer {self.name}?')
        print('This cannot be undone!\nEnter this to continue:')
        confirmation = self.game_manager.get_user_input(
            'I am sure I want to transfer my pet.'
        )
        if confirmation.strip() == 'I am sure I want to transfer my pet.':
            transfer_time = randrange(10)

            print(f'\nTransferring {self.name}...')
            print(f'This should take about {transfer_time} second(s).')
            for i in tqdm(range(transfer_time), desc='Transferring'):
                time.sleep(0.25)
            print(f'{self.name}, a {self.kind}, has been transferred.')
            print(f'Goodbye, {self.name} :(')
            time.sleep(2)
            self.end(False)
        else:
            print(f'Transfer of {self.name} has been cancelled.')

    def add_to_stat(self, attr, value=100, display=True):
        attribute = self.stats[attr]
        attribute['val'] += value
        if 'max' in attribute and attribute['val'] >= attribute['max']:
            attribute['val'] = attribute['max']
        if 'min' in attribute and attribute['val'] <= attribute['min']:
            attribute['val'] = attribute['min']
        if display:
            print(attr + " is now at " + str(attribute['val']))

        if attr == 'snack meter' and self.stats['snack meter']['val'] > 5:
            print(f'{self.name} has died from severe sugar intake. :(')
            self.end()

    def play_game1(self):
        self.game_manager.display_fig("DIRECTION GAME")

        answers = ['L', 'R']
        L_or_R = choices(answers)[0]  # choices() returns an array

        guess = self.game_manager.get_user_input(
            'guess if i will go left or right!(L/R)'
        )

        while guess not in answers:
            print('that\'s not a valid answer!')
            guess = self.game_manager.get_user_input(
                'guess if i will go left or right!(L/R)'
            )

        if guess == L_or_R:
            print('congrats! you were right!<( ^ o ^)>')
            self.add_to_stat("happiness", randrange(30))
        else:
            print('sorry. you were wrong. <( o  o )>')
            self.add_to_stat("happiness", randrange(20))

    def end(self, is_dead=True):
        """End the player's time for the pet.

        Keyword arguments:
        is_dead -- bool (default is True)

        If this function is called because the pet died from something, then further arguments are not needed, just call end(). Otherwise, let False be the only parameter: end(False).
        """
        self.game_manager.display_fig("THE END")
        if is_dead:
            print(f'{self.name} lived for {self.lifetime} minute(s).')
            print('please type \'quit\' to exit.')
        else:
            print(
                f'you took care of {self.name} for {self.lifetime} minute(s).'
            )
        time.sleep(5)
        self.is_alive = False
