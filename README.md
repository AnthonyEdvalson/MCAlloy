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

Create complex statements like `d = math.sqrt(x ** 2 + y ** 2)` and have them run flawlessly in Minecraft, MCAlloy takes care of the heavy lifting

3. Consistency

Remember when /testfor was removed? Because MCAlloy compiles your code, it can target multiple Minecraft versions, and change how it writes commands
depending on updates to Minecraft, so you don't have to worry about a new update making you rewrite everything


# How It Works

MCAlloy runs Python in the same way your computer does. MCAlloy compiles your scripts and translates the bytecode into minecraft commands. This way you have
the full power of Python available in your datapacks without having to learn a new language.

For an in-depth look at MCAlloy's inner workings, look at README_TECHNICAL.md


# What can it do?

In general, MCAlloy can handle everything Python can handle. Here's some of the nicer features MCAlloy has to offer

- Variables
- Scope
- If Conditions
- For Loops
- While Loops
- Iterators
- Some builtins like print()
- Functions

On top of all that, MCAlloy comes with a handful of libraries that let you call minecraft commands with functions easily

```python
from MCAlloy import blocks
from MCAlloy.entities import players

x = players.nearest.position.x
y = players.nearest.position.y
for z in range(0, 15):
    blocks.set(x, y, z, "dirt")
```

And if you want to run a very specific command, you can always inject them directly by putting them in a string starting with a slash

```python
x = 10
y = 12
for z in range(0, 15):
    '/execute as @a[tag=alive] run kill @s' 
```

If you need to access a specific variable in an injected command, put the variable name in angle brackets.

```python
def refresh_scoreboard(kills):
    score = 5 * kills
    '/execute store result score Players Score run data get <score>'
```

MCAlloy translates the angle brackets to the actual NBT location

```
execute store result score Players Score run data get ArmorItems[0].tag.Names.score.v
```

# What can't it do?

There's some limitations to MCAlloy compared to Python

- Missing most of the standard library
- No async calls
- No runtime string concatenation or modification
- Garbage collection only uses reference counting

These are some features currently in the works

- Imports
- Classes
- Objects
- Floats
- Generator functions
- Dictionaries
- Tuples
- Lists
- Builtin functions like abs(), int(), and min()
- *args and **kwargs
- Typing
- With

And here are some of the planned libraries to be added

- math
- collections
- bisect
- types
- copy
- enum
- random
- itertools
- typing
- sys
- abc
- traceback
- atexit

I'd appreciate any feedback on which features you'd like to see added. 