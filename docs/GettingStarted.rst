..  _GettingStarted:

Getting Started
===============

Here's a simple python script that prints the first 5 fibonacci numbers

::
    # fib.py

    def fib(n):
       if n < 2:
            return 1

        return fib(n-1) + fib(n-2)

    i = 0
    while i < 5:

        i += 1
        print(fib(i))

This code will run great in Python, but not in Minecraft. To get it to run in Minecraft we need to use MCAlloy to
translate from .py files, to .mcfunction files. Make sure MCAlloy is already :ref:`GettingStarted` installed.

First, the script should be placed in a hierarchy like this

 * datapack
   * namespace
     * fib.py

From here you have two options

1. Run MCAlloy from the command line
2. Run MCAlloy from the .exe

Both options have all the same features, the .exe is provided as a convenience for those who aren't used to the command line


Running from the Command Line
-----------------------------

Running MCAlloy from the command line is recommended for those who are comfortable using the command line

Navigate so that your current directory is the datapack folder, and run ``mcalloy auto`` the code inside that folder will be
compiled to mcfunctions, and written to a new datapack inside of your most recently played save.


Running from the .exe
---------------------

Running MCAlloy from the .exe is recommended for developers who are used to working with an IDE

Run MCAlloy.exe and select the folder you'd like to compile, in this case you want to select the datapack folder we just made.
It will save the compiled datapack in your mose recently played save by default, but this target directory can be changed in the UI


Using the Datapack in Minecraft
-------------------------------

Run Minecraft as you normally would, and play the world that MCAlloy saved the datapack in. To test if everything worked,
run the command /function namespace:fib. You should see the following appear in chat

::
    1
    2
    3
    5
    8

You just wrote a datapack in Python!
