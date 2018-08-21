#Credits to https://codereview.stackexchange.com/users/1659/winston-ewert

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def ordinal(num):
    num = int(num)
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix