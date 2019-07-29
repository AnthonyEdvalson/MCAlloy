# MCAlloy

MCAlloy is a tool allows datapack creators to write datapacks in python.

```python
# example/main.py
 
def fib(n):
    if n < 2:
        return 1
    return fib(n - 2) + fib(n - 1)
 
print(fib(5))
```

MCAlloy converts this to a datapack, and if you import it into a Mincraft world and run `/function example.main` it will print out the 5th fibonacci number

# Benefits

1. Brevity

No more `scoreboard players add @s score 5`, say exactly what you mean `score += 5`. You don't have to dig through console logs to see why your functions wont load
Also, because it's python, you can code and compile straight from your IDE of choice, and get that sweet sweet error checking

2. Flexibility

Create complex statements like `d = math.sqrt(x ** 2 + y ** 2)` and have them run flawlessly in Minecraft, Alloy takes care of the heavy lifting

3. Consistency

Remember when /testfor was removed? Because MCAlloy compiles your code, it can target specific minecraft versions, and you don't have to worry that the next update will make your work obsolete.


# How It Works

MCAlloy runs Python in the same way your computer does. MCAloy takes the scripts compiled bytecode, and translates it into commands in mcfunctions. That way you have
the full power of Python available in your datapacks without having to learn a new language.

