# MCAlloy

MCAlloy is a revolutionary tool lets you write Minecraft datapacks in Python.

```python
# example/main.py
 
def fib(n):
    if n < 2:
        return 1
    return fib(n - 2) + fib(n - 1)
 
print(fib(5))
```

MCAlloy compiles Python to a Minecraft datapack. If you import it into a Minecraft world and run `/function example.main` it will print out the 5th fibonacci number


# Benefits

1. Brevity

No more `scoreboard players add @s score 5`, say exactly what you mean `score += 5`. Fewer keystrokes means less errors, and faster development.
Also, because it's Python, you can code and compile in your IDE of choice to get that sweet sweet error checking.

2. Power

Create complex statements like `d = math.sqrt(x ** 2 + y ** 2)` and have them run flawlessly in Minecraft, Alloy takes care of the heavy lifting

3. Consistency

Remember when /testfor was removed? Because MCAlloy compiles your code, it can target multiple Minecraft versions, so you don't have to worry that 
a new update will change command syntax and make your work obsolete.


# How It Works

MCAlloy runs Python in the same way your computer does. MCAlloy compiles your scripts and translates the bytecode into minecraft commands. This way you have
the full power of Python available in your datapacks without having to learn a new language.

For an in-depth look at MCAlloy's inner workings, look at README_TECHNICAL.md


# What Can It Do?

In general, MCAlloy can handle everything Python can handle. Here's some of the nicer featuers MCAlloy has to offer

- Variables
- Scope
- Classes
- Objects
- Typing
- If Conditions
- For Loops
- While Loops
- Iterators
- Most builtins like print()
- Functions
- Imports

On top of all that, MCAlloy comes with a handful of libraries that let you call minecraft commands straight from your code

```python
from MCAlloy import blocks

x = 10
y = 12
for z in range(0, 15):
    blocks.set(x, y, z, "dirt")
```


# What Can't It Do?

There's some limitations to MCAlloy compared to Python, since it's running in Minecraft.

It is:
- Missing most of the standard library
- No async calls
- No string concatenation or modification, but they can be used as constants

These are planned features currently in the works

- floats
- math library
- generator functions
- dictionaries
- tuples
- lists
- classes

