import time
import random
import threading

pettype = input('Welcome to the Pet Shop. We have pet rocks, pet fish,  ')
petname = input('what do you name your new buddy?\n')
energy = 80
happy = hunger = 100
alive = True

print(f'this is {petname} the {pettype}.')
print('<( o  o )>')
print('you need to take care of it.')
print('type actions to see all the actions!')


def periodic_stat_change():
    global last_change
    global energy
    global hunger
    global happy

    while True:
        if time.time() - last_change > 60:
            last_change = time.time()
            energy -= random.randrange(30)
            hunger -= random.randrange(30)
            happy -= random.randrange(30)


last_change = time.time()
thread = threading.Thread(target=periodic_stat_change)
thread.start()

while alive:
    command = input()

    if command == 'stats':
        print(f'energy: {energy}\nhappy: {happy}\nhunger: {hunger}')

    elif command == 'sleep':
        print(f'<(  u _ u )>\n{petname} is sleeping...')
        time.sleep(random.randrange(60))
        print(f'<( o  o )>\n{petname} is awake!')
        energy += 30

    elif command == 'feed':
        print('   bread\n    ¯\_( o  o )')
        time.sleep(0.5)
        print('<( ^ o ^ )>\nyummy!')
        hunger += random.randrange(40)

    elif command == 'actions':
        print('actions include:\nsleep\npet\nfeed\nstats\nfeelings\n')

    elif command == 'pet':
        print('^( o  o )>')
        time.sleep(0.5)
        print('<( o  o )^')
        happy += random.randrange(30)

    elif command == 'feelings':
        if happy > 60:
            print('<( ^ ^ )>\ni am very happy!')
        elif happy < 60:
            print('<( o  o )>\nfeeling okay!')
    elif energy < 50:
        print("<(-  -)> i'm tired")
    elif hunger < 50:
        print("<(o  O  o)> i'm hungry")
    elif happy < 50:
        print("<(T  T)> i'm sad")
    elif energy < 0 or hunger < 0 or happy < 0:
        if energy < 0:
            print(f'{petname} has died due to being too tired. :(')
        elif hunger < 0:
            print(f'{petname} has died due to hunger. :(')
        elif happy < 0:
            print(f'{petname} has died due to sadness. :(')
        alive = False
