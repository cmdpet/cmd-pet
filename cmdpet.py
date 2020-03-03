import time
import random
import threading
import webbrowser
from pyfiglet import figlet_format as fig

logo = fig("CMD-PET")
print(logo)

version = '1.3.0'
print(f'<( o  o )> (v{version})\nby VukAnd and hellogoose\n')

pettype = input('Welcome to the Pet Shop. We have pet rocks, pet fish, pet dogs and pet cats. What would you like?\n')
if pettype != 'pet rock' or 'pet fish' or 'pet dog' or 'pet cat' or 'rock' or 'fish' or 'dog' or 'cat':
    print('We don\'t have that...')
petname = input('what do you name your new buddy?\n')
energy = 80
happy = hunger = 100
alive = True
snack_meter = 1

print(f'this is {petname} the {pettype}.')
print('<( o  o )>')
print('you need to take care of it.')
print('type actions to see all the actions!')


def periodic_stat_change():
    global last_change
    global energy
    global hunger
    global happy
    global snack_meter

    while True:
        if time.time() - last_change > 60:
            last_change = time.time()
            if pettype == 'rock' or pettype == 'pet rock':
                energy -= 1
                hunger -= 1
                happy -= 1
                snack_meter -= 5
            else:
                energy -= random.randrange(30)
                hunger -= random.randrange(30)
                happy -= random.randrange(30)
                snack_meter -= 0.5


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
        energy += random.randrange(30)

    elif command == 'feed':
        print('   bread\n    ¯\_( o  o )')
        time.sleep(0.5)
        print('<( ^ o ^ )>\nyummy!')
        hunger += random.randrange(30)

    elif command == 'feed bread':
        print('   bread\n    ¯\_( o  o )')
        time.sleep(0.5)
        print('<( ^ o ^ )>\nyummy!')
        hunger += random.randrange(30)

    elif command == 'feed snack':
        print('   snack\n    ¯\_( o  o )')
        time.sleep(0.5)
        print('<( ^ o ^ )>\nyummy and sweet! this makes me happy!')
        hunger += random.randrange(15)
        snack_meter += 1

    elif command == 'actions':
        print('actions include:\nsleep\npet\nfeed (snack/bread)\nstats\nfeelings\ntransfer\nfor more commands:\nmanual\n')

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

    elif command == 'transfer':
        transferSure = input(f'\nare you sure you want to transfer {petname}?\nthis cannot be undone!\ntype this to continue:\ni am sure i want to transfer my pet.\n')
        if transferSure == 'i am sure i want to transfer my pet.':
            transferTime = random.randrange(10)
            print(f'\nTransferring {petname}...\nthis should take about {transferTime} second(s).')
            time.sleep(transferTime)
            print(f'{petname} the {pettype} has been transferred.\ngoodbye, {petname} :(')
            time.sleep(2)
            quit()
        else:
            print(f'Transfer of {petname} has been cancelled.')

    elif command == 'manual':
        manualSure = input(f'open manual in your browser? (y/n)')
        if manualSure == 'y':
            print('okay, opening now...')
            webbrowser.open('https://github.com/cmdpet/cmd-pet/wiki', new=0, autoraise=True)
        else:
            print('alright.')
    else:
        print(f'{petname} doesn\'t understand that command.')
    
    if energy < 50:
        print('<(-  -)> i\'m tired')
    if hunger < 50:
        print('<(o  O  o)> i\'m hungry')
    if happy < 50:
        print('<(T  T)> i\'m sad')
    if energy < 0 or hunger < 0 or happy < 0 or snack_meter < 6 or energy < 1 or hunger < 1 or happy < 1 or snack_meter < 5:
        if energy < 0:
            print(f'{petname} has died due to being too tired. :(')
        elif hunger < 0:
            print(f'{petname} has died due to hunger. :(')
        elif happy < 0:
            print(f'{petname} has died due to sadness. :(')
        elif snack_meter < 6 or snack_meter < 5:
            print(f'{petname} has died due to you feeding it too many snacks. :(')
        alive = False
    if energy > 100 or hunger > 100 or happy > 100 or snack_meter < 1:
        if energy > 100:
            energy = 100
        elif hunger > 100:
            hunger = 100
        elif happy > 100:
            happy = 100
        elif snack_meter < 1:
            snack_meter = 1
