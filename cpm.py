# cPassMan v2.0
# Password manager
# autor https://github.com/m80b33

import os, time, re, random, string
from getpass import getpass

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


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
    print('(1) Open Entries List')
    print('(2) Add New Entry')
    print('(3) Options')
    print('(4) Exit\n')


def pwgen(length):
    kl = string.digits + string.ascii_letters + '@#$%&*_'
    w = []
    while len(w) < length:
        c = random.choice(kl)
        w.append(c)
    return ''.join(w)


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(data, key):
    key = SHA256.new(key).digest()
    data = pad(data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(data)


def decrypt(data, key):
    key = SHA256.new(key).digest()
    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    p = cipher.decrypt(data[AES.block_size:])
    return p.rstrip(b"\0")


def login():
    clear()
    print(logo)
    if os.path.exists('base.pwd'):
        try:
            key = bytes(getpass('You Super Password: '), encoding="UTF-8")
            file = open('base.pwd', 'rb').read()
            decrypt(file, key).decode('utf-8')
        except:
            print('Oops, try again!')
            login()
        clear()
        print(logo)
        menu()
        main(key)
    else:
        while True:
            key = bytes(getpass('New base will be create!\nYour password: '), encoding="UTF-8")
            confirm = bytes(getpass('Confirm password: '), encoding="UTF-8")
            if key == confirm:
                clear()
                with open('base.pwd', 'wb') as f:
                    data = bytes('cPassMan {3}{0:^24} {1:^24} {2:^24} {3}{4:-<24} {4:-<24} {4:-<24} {3}'.format('Login', 'Password', 'Service', '\n', '-'), encoding="UTF-8")
                    cdata = encrypt(data, key)
                    f.write(cdata)
                    f.close()
                    print('\nPasswords database successfully created and encrypted with Super Password\n')
                print(logo)
                menu()
                main(key)
                break
            else:
                print('Oops, try again!')


def main(key):
    while True:
        k = input('> ')
        if k == '4':
            clear()
            print('''cPassMan v2.0
console Password manager
https://github.com/m80b33\n\n\nBye!\n''')
            time.sleep(5)
            clear()
            break

        elif k == '3':
            try:
                print('(1) Change Super Password.\n(2) Open base file with text editor(not safe!).')
                while True:
                    i = input('\n> ')
                    if i == '2':
                        file = open('base.pwd', 'rb').read()
                        data = decrypt(file, key).decode('utf-8')
                        tmp = open('tmp', 'w').write(data)
                        os.system('notepad tmp && del tmp')
                        clear()
                        print(logo)
                        menu()
                        break
                    elif i == '1':
                        file = open('base.pwd', 'rb').read()
                        data = decrypt(file, key)
                        while True:
                            okey = bytes(getpass('Old Super Password: '), encoding="UTF-8")
                            if okey == key:                                
                                nkey = bytes(getpass('New Super Password: '), encoding="UTF-8")
                                confirm = bytes(getpass('Confirm new Super Password: '), encoding="UTF-8")
                                if nkey == confirm:
                                    clear()
                                    key = nkey
                                    with open('base.pwd', 'wb') as f:
                                        cdata = encrypt(data, key)
                                        f.write(cdata)
                                        f.close()
                                        print('\nSuper Password successfully changed!\n')
                                    break
                                else:
                                    print('New Super Password not confirmed!')
                            else:
                                print('Wrong Old Super Password!')
                        clear()
                        print(logo)
                        menu()
                        break
                    else:
                        print('\nInvalid choice!\n')
            except:
                 print('\nWrong Super Password!\n')
                 login()

        elif k == '2':
            try:
                file = open('base.pwd', 'rb').read()
                d = decrypt(file, key).decode('utf-8')
                clear()
                s = input('\nTo which service credentials: ' )
                l = input('Login: ' )
                p = ''
                i = input('Do you want to (c)reate your own password or you need help to (g)enerate it?\n(c/g)?: ' )
                if i == 'c':
                    p = input('Password: ' )
                    data = bytes(d + '{0:<24} {1:<24} {2:<24}\n'.format(l, p, s), encoding='UTF-8')
                    cdata = encrypt(data, key)
                    with open('base.pwd', 'wb') as f:
                        f.write(cdata)
                        f.close()
                        print('Data recorded!')
                    clear()
                    print(logo)
                    menu()
                elif i == 'g':
                    while True:
                        length = input('Enter the password length(24 or less): ' )
                        try:
                            if int(length) <= 24:
                                p = pwgen(int(length))
                                data = bytes(d + '{0:<24} {1:<24} {2:<24}\n'.format(l, p, s), encoding='UTF-8')
                                cdata = encrypt(data, key)
                                with open('base.pwd', 'wb') as f:
                                    f.write(cdata)
                                    f.close()
                                    print('Data recorded!')
                                clear()
                                print(logo)
                                menu()
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
            except:
                print('\nWrong Super Password!\n')
                login()

        elif k == '1':
            try:
                clear()
                file = open('base.pwd', 'rb').read()
                data = decrypt(file, key)
                print('\n' + data.decode('utf-8') + '\n')
                menu()
            except:
                print('\nWrong Super Password!\n')
                login()

        else:
            print('\nInvalid choice, try again!\n')


if __name__ == '__main__':
    login()
