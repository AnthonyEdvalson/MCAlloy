def fib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)


i = 0
while i < 5:
    i += 1
    print(fib(i))

"""

def print(x):
    '/tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}'

def f(x):
    return x + 1

a = 55
b = -3

# Function call in if statement
if f(a + 5 * b) < 42:
    if a == 55:
        a /= 5
    else:
        print("hey")

if 5 == 3:
    pass
elif 3 == 12:
    pass
else:
    if 4 == 4:
        if 5 == 3:
            pass
        else:
            b += 55

c = a + b
c += 5

# Two function calls in one eval, and nested calls
print(a * f(3 + b) - f(f(60) * b))
"""