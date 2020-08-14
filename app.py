# Password manager
# autor https://github.com/m80b33


import os, random, string
from time import sleep
from datetime import datetime
from getpass import getpass
from termcolor import cprint
from sys import platform

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


# Windows title
if platform == 'win32':
    os.system('title ' + 'cPassMan')
    BASEDIR = os.path.expanduser("~")
    BACKUPDIR = BASEDIR + '\\PWDBACKUP'
elif platform == 'linux':
    BASEDIR = os.path.expanduser("~")
    BACKUPDIR = BASEDIR + '/PWDBACKUP'

BASEFILE = os.path.join(BASEDIR, 'base.pwd')

if not os.path.exists(BACKUPDIR):
    try:
        os.system(f'mkdir {BACKUPDIR}')
    except:
        cprint('Cant create \'PWDBACKUP\' dir!', 'red')

BACKUPFILE = os.path.join(BACKUPDIR, 'base{}'.format(datetime.now().strftime("%H%M%d%m%y")))


#Logo
def logo():
    sleep(0.5)
    if platform == 'win32':
        os.system('cls')
    elif platform == 'linux':
        os.system('clear')
    cprint(r'''
█▀▀ ▒█▀▀█ █▀▀█ █▀▀ █▀▀ ▒█▀▄▀█ █▀▀█ █▀▀▄
█░░ ▒█▄▄█ █▄▄█ ▀▀█ ▀▀█ ▒█▒█▒█ █▄▄█ █░░█
▀▀▀ ▒█░░░ ▀░░▀ ▀▀▀ ▀▀▀ ▒█░░▒█ ▀░░▀ ▀░░▀
    ''', 'blue')


# Progress Bar
def progress():
    r = 40
    items = list(range(0, r))
    l = len(items)
    for i, item in enumerate(items):
        sleep(0.02)
        filled = int(r * (i + 1) // l)
        bar = '█' * filled + ' ' * (r - filled)
        print(f'\r{bar}', end = '\r')


# Menu
def menu():
    cprint(':> Show Entries List (1)', 'yellow')
    cprint(':> Add New Entry (2)', 'yellow')
    cprint(':> Options (3)', 'yellow')
    cprint(':> Exit (4)\n', 'yellow')


def logout():
    logo()
    cprint('''        cPassMan v1.3
console Password manager
https://github.com/m80b33\n
                           2020\n''', 'blue')
    sleep(5)
    
    if platform == 'win32':
        os.system('cls')
    elif platform == 'linux':
        os.system('clear')


def ic_error():
    cprint('\nInvalid choice, try again!\n', 'red')


# New password generation
def pwgen(length):
    word = []
    while len(word) < length:
        word.append(random.choice(string.digits + string.ascii_letters + '@#$%&*_'))
    return ''.join(word)


# Crypto part
#############
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
#############


# Key check
def getkey():
    return bytes(getpass('Enter your Super Password to continue:> '), encoding="UTF-8")


# Playing with base file
def baf(data, key):
    cdata = encrypt(data, key)
    with open(BASEFILE, 'wb') as f:
        f.write(cdata)
        f.close()


# Do the work
def job(key):
    while True:
        k = input(':> ')
        if k == '4':
            logout()
            break
        elif k == '3':
            logo()
            try:
                def submenu():
                    cprint(':> Back to main Menu(1)\n:> Change Super Password (2)\n:> Open base file with text editor (3)\n:> Make base backup (4)\n:> Restore from backup (5)\n', 'yellow')
                while True:
                    submenu()
                    i = input(':> ')
                    if i == '5':
                        logo()
                        cprint('Enter the full path to the backup file\n', 'yellow')
                        fp = input(':> ')
                        if os.path.exists(fp):
                            os.system(f'copy /Y {fp} {BASEFILE}')
                            logo()
                            cprint('The database file is recovered!', 'green', attrs=['bold'])
                            cprint('The super password from the recovered database may not match the one entered earlier.', 'green', attrs=['bold'])
                            cprint('Make sure you remember it!\n', 'red', attrs=['bold'])
                        else:
                            logo()
                            cprint('The path to the file or it name is incorrect!', 'red')
                    elif i == '4':
                        if platform == 'win32':
                            os.system(f'copy {BASEFILE} {BACKUPFILE}')
                        elif platform == 'linux':
                            os.system(f'cp {BASEFILE} {BACKUPFILE}')
                        logo()
                        cprint(f'Backup is created to {BACKUPDIR}!\n', 'green', attrs=['bold'])
                    elif i == '3':
                        file = open(BASEFILE, 'rb').read()
                        data = decrypt(file, key).decode('utf-8')
                        tmp = open('tmp', 'w').write(data)
                        if platform == 'win32':
                            os.system('notepad tmp && del tmp')
                        else:
                            os.system('nano tmp && del tmp')
                        logo()
                    elif i == '2':
                        file = open(BASEFILE, 'rb').read()
                        data = decrypt(file, key)
                        while True:
                            logo()
                            okey = bytes(getpass('Old Super Password:> '), encoding="UTF-8")
                            if okey == key:
                                nkey = bytes(getpass('New Super Password:> '), encoding="UTF-8")
                                confirm = bytes(getpass('Confirm new Super Password:> '), encoding="UTF-8")
                                if nkey == confirm:
                                    key = nkey
                                    baf(data, key)
                                    break
                                else:
                                    cprint('New Super Password not confirmed!', 'red')
                            else:
                                cprint('Wrong Old Super Password!', 'red')
                        logo()
                        cprint('Super Password successfully changed!\n', 'green', attrs=['bold'])
                    elif i == '1':
                        logo()
                        menu()
                        break
                    else:
                        ic_error()
            except:
                 cprint('\nWrong Super Password!\n', 'red')
                 main()
        elif k == '2':
            try:
                file = open(BASEFILE, 'rb').read()
                d = decrypt(file, key).decode('utf-8')
                logo()
                dn = datetime.now().strftime("%d.%m.%y")
                s = input('\nTo which service credentials:> ' )
                l = input('Login:> ' )
                print('Do you want to (c)reate your own password or you need help to (g)enerate it?\n(c/g)?:> ')
                while True:
                    i = input(':> ' )
                    if i == 'c':
                        p = input('Password:> ' )
                        data = bytes(d + '{0:<24} {1:>24} {2:>24} {3:>8}\n'.format(l, p, s, dn), encoding='UTF-8')
                        baf(data, key)
                        logo()
                        cprint(f'User \'{l}\' with your password added!\n', 'green', attrs=['bold'])
                        menu()
                        break
                    elif i == 'g':
                        print('Enter the password length (24 or less):> ')
                        while True:
                            length = input(':> ' )
                            try:
                                if int(length) <= 24:
                                    p = pwgen(int(length))
                                    data = bytes(d + '{0:<24} {1:>24} {2:>24} {3:>8}\n'.format(l, p, s, dn), encoding='UTF-8')
                                    baf(data, key)
                                    logo()
                                    cprint(f'Password generated, user \'{l}\ added!\n', 'green', attrs=['bold'])
                                    menu()
                                    break
                                else:
                                    cprint('\nInvalid password length (should be 24 or less)!\n', 'red')
                            except:
                                cprint('\nInvalid password length (should be 24 or less)!\n', 'red')
                        break
                    else:
                        ic_error()
            except:
                cprint('\nWrong Super Password!\n', 'red')
                main()
                break
        elif k == '1':
            try:
                logo()
                file = open(BASEFILE, 'rb').read()
                data = decrypt(file, key)
                cprint('\n' + data.decode('utf-8') + '\n', 'white')
                cprint(':> Back to main Manu(1)\n', 'yellow')
                while True:
                    i = input(':> ')
                    if i == '1':
                        logo()
                        menu()
                        break
                    else:
                        ic_error()
            except:
                cprint('\nError!\n', 'red')
                main()
                break
        else:
            ic_error()


# Main
def main():

    cprint(':> Login (1)', 'yellow')
    cprint(':> Exit (4)\n', 'yellow')

    while True:
        hello = input(':> ')
        if hello == '1':
            while True:
                if os.path.exists(BASEFILE):
                    while True:
                        try:
                            logo()
                            key = getkey()
                            file = open(BASEFILE, 'rb').read()
                            decrypt(file, key).decode('utf-8')
                            break
                        except:
                            cprint('Oops, try again!', 'red')
                    logo()
                    menu()
                    job(key)
                    break
                else:
                    while True:
                        cprint(f'New base will be create to {BASEDIR}!', 'red', attrs=['bold'])
                        key = getkey()
                        confirm = bytes(getpass('Confirm Password:> '), encoding="UTF-8")
                        if key == confirm:
                            progress()
                            data = bytes('{3}{0:^24} {1:^24} {2:^24} {5:^8} {3}{4:-<24} {4:-<24} {4:-<24} {4:-<8} {3}'.format('Login', 'Password', 'Service', '\n', '-', 'Data'), encoding="UTF-8")
                            baf(data, key)
                            logo()
                            cprint('\nPasswords database successfully created and encrypted with Super Password\n', 'green', attrs=['bold'])
                            menu()
                            job(key)
                            break
                        else:
                            cprint('Oops, try again!', 'red')
            break
        elif hello == '4':
            logout()
            break
        else:
            ic_error()


if __name__ == '__main__':

    # Welcome Z0ne
    ##############

    logo()
    cprint('     console Password Manager v3.0\n', 'yellow')
    progress()
    cprint('\n\n            Welcome, Sir!\n', 'blue', attrs=['bold'])

    ##############

    main()
