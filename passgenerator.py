import random

print('GEnerate your password here')

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*().,?_1234567890'
num = input('Amount of password to generate: ')
num = int(num)

length = input('Input your password length: ')
length = int(length)

print('\nHere are your passwords : ')

for pwd in range(num):
    passwords = ''
    for c in range(length):
        passwords += random.choice(chars)
    print(passwords)