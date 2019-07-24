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


