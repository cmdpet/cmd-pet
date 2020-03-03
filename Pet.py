import time
from random import randrange
from collections import defaultdict
from threading import Thread, Event


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

    def __init__(self, name, kind, energy, happiness, hunger):
        self.name = name
        self.kind = kind

        self.stats = defaultdict(dict)
        for (attribute, detail), val in self.raw_stats.items():
            self.stats[attribute][detail] = val

        self.stats["energy"]["val"] = energy
        self.stats["happiness"]["val"] = happiness
        self.stats["hunger"]["val"] = hunger

        self.thread_event = Event()
        self.thread_event.set()

        self.thread = Thread(
            target=self.decrease_stats, args=(self.thread_event,)
        )
        self.thread.start()

    def decrease_stats(self, thread_event):
        """Decreases stat values every 60 seconds.

        Keyword arguments:
        thread_event -- a threading.Event() object

        Whilst the thread_event is set to be true, all of the stats of the pet will decrease, either randomly or with a set value, after every 60 seconds. The lifetime is also recorded in minutes. After each change, all values will be evaluated with the check_status() method to ensure that the pet is indeed still alive. Once the game ends, thread_event is then set to false, which ends the while loop. 
        """
        frequency = 60
        last_change = time.time()
        while thread_event.is_set():
            if (time.time() - last_change) > frequency:
                last_change = time.time()
                self.lifetime += 1
                for attr in self.stats:
                    if attr == 'snack meter':
                        self.add_to_stat(attr, -1, False)
                    else:
                        self.add_to_stat(attr, (-1 * randrange(30)), False)

                self.check_status()

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
        time.sleep(randrange(60))

    def fed(self):
        print('    bread\n    ^  ^\n( o  o )')
        time.sleep(0.5)
        print('<( o <ead> o )>\nyummy!')
        self.add_to_stat("hunger", randrange(15))
        self.add_to_stat("snack meter", 1)

    def pet(self):
        print('^( o  o )>')
        time.sleep(0.5)
        print('<( o  o )^')
        self.add_to_stat("happiness", randrange(30))

    def feelings(self):
        threshold = self.stats['happiness']['max'] / 2
        if self.stats['happiness']['val'] >= threshold:
            print('<( ^ ^ )>\ni am very happy!')
        elif self.stats['happiness']['val'] < threshold:
            print('<( o  o )>\nfeeling okay!')

    def transfer(self):
        transferSure = input(f'\nAre you sure you want to transfer {self.name}?\nThis cannot be undone!\nEnter this to continue:\nI am sure I want to transfer my pet.\n')
        if transferSure == 'I am sure I want to transfer my pet.':
            transferTime = randrange(10)
            print(f'\nTransferring {self.name}...\nThis should take about {transferTime} second(s).')
            time.sleep(transferTime)
            print(f'{self.name}, a {self.kind}, has been transferred.\nGoodbye, {self.name} :(')
            time.sleep(2)
            quit()
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
            print(f'{self.name} has died from severe overeating. :(')
            self.die()

    def check_status(self):
        if self.stats['energy']['val'] < 50:
            print('<(-  -)> i\'m tired')
        if self.stats['hunger']['val'] < 50:
            print('<(o  O  o)> i\'m hungry')
        if self.stats['happiness']['val'] < 50:
            print('<(T  T)> i\'m sad')

        if self.stats['energy']['val'] < 0:
            print(f'{self.name} has died due to being too tired. :(')
            self.die()
        elif self.stats['hunger']['val'] < 0:
            print(f'{self.name} has died due to hunger. :(')
            self.die()
        elif self.stats['happiness']['val'] < 0:
            print(f'{self.name} has died due to sadness. :(')
            self.die()
        elif self.stats['snack_meter']['val'] > 5:
            print(f'{self.name} has died from severe overeating. :(')
            self.die()

    def die(self):
        print(f'your pet lived for {self.lifetime} minutes.')
        self.is_alive = False
