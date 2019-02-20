# cPassMan v1.0
# Password manager
# autor m80b33

import os, time, re, random, string

os.system('title ' + 'cPassMan')

logo = r'''
console Password Manager
      __________                         _____
  ____\______   \_____    ______ ______ /     \ _____    ____
_/ ___\|     ___/\__  \  /  ___//  ___//  \ /  \\__  \  /    \
\  \___|    |     / __ \_\___ \ \___ \/    Y    \/ __ \|   |  \
 \___  >____|    (____  /____  >____  >____|__  (____  /___|  /
     \/               \/     \/     \/        \/     \/     \/

                          Welcome!!!
#################################################################
'''

def clear():
    time.sleep(1.5)
    os.system('cls')


def menu():
    print('(1) Open Passwords List')
    print('(2) Add New Password')
    print('(3) Options')
    print('(4) Exit\n')

clear()
print(logo)
menu()


def pwgen(length):
    kl = string.digits + string.ascii_letters + '@#$%&*_'
    w = []
    while len(w) < length:
        c = random.choice(kl)
        w.append(c)
    return ''.join(w)


def basecrt():
    if not os.path.exists('base.pwd'):
        with open('base.pwd', 'w') as f:
            f.write('{0:^24} {1:^24} {2:^24} {3}'.format('Login', 'Password', 'Service', '\n'))
            f.write('{0:-<24} {0:-<24} {0:-<24} {1}'.format('-','\n'))
        print('\nPasswords database successfully created!\n')

    else:
        print('\nPasswords database already exists!\n')


def main():
    while True:
        k = input('> ')

        if k == '4':
            clear()
            print('''cPassMan v1.0
console Password manager
https://github.com/hatingman\n\n\nBye!\n''')
            time.sleep(5)
            clear()
            break

        elif k == '3':
            print('(1) First Start. Create new base file.\n(2) Open base file with text editor.')
            i = input('\n> ')

            if i == '2':
                os.system('notepad base.pwd')
                clear()
                print(logo)
                menu()

            elif i == '1':
                basecrt()
                clear()
                print(logo)
                menu()

            else:
                print('\nInvalid choice!\n')

        elif k == '2':
            try:
                with open('base.pwd', 'a') as f:
                    clear()

                    s = input('\nTo which service credentials: ' )
                    l = input('Login: ' )
                    p = ''
                    i = input('Do you want to (c)reate your own password or you need help to (g)enerate it?\n(c/g)?: ' )

                    if i == 'c':
                        p = input('Password: ' )
                    elif i == 'g':
                        while True:
                            length = input('Enter the password length(24 or less): ' )
                            try:
                                if int(length) <= 24:
                                    p = pwgen(int(length))
                                    print('Done!')
                                    break
                                else:
                                    print('\nInvalid password length!\n')
                            except:
                                print('\nInvalid password length!\n')

                    else:
                        print('\nInvalid choice, try again!\n')
                        clear()
                        print(logo)
                        menu()

                    f.write('{0:<24} {1:<24} {2:<24}\n'.format(l, p, s))
                    f.close()
                    print('Data recorded!')
                    clear()
                    print(logo)
                    menu()
            except:
                print('\nThere are no base.pwd file in a folder. \nIf you want to create new base file choose (1) in main manu!\n')
                menu()

        elif k == '1':
            try:
                clear()
                f = open('base.pwd', 'r')
                print('\n' + f.read() + '\n')
                menu()
            except:
                print('\nThere are no base.pwd file in a folder. \nIf you want to create new base file choose (3) in main manu!\n')
                menu()

        else:
            print('\nInvalid choice, try again!\n')


if __name__ == '__main__':
    main()
