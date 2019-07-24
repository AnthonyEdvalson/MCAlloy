# MCALLOY - TECHNICAL DETAILS

This document contains some details on the inner workings of MCAlloy, the information here isn't necessary to use MCAlloy.
if you are interested in how MCAlloy works, this contains a full overview of the system. The document is designed to be read by people who are familiar with Python, datapacks, compilers, and the Python virtual machine

## EXECUTION

Before looking in to the compilation, it is important to understand the method by which the code will execute in Minecraft.

Python is a stack based language, all computation and execution is done in some way on a stack. For example, here is how Python interprets `a + b`

```
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```

This is Python bytecode, a series of instructs that will run on the stack.
 Lets assume a=2 and b=3. If the above code is executed, the value of "a" is loaded to the stack, abd then the value of "b". So after the first two instructions, the stack looks like

```

 -----
 |   |
 | 3 |
 | 2 |
 -----
```

Then the BINARY_ADD says to add the top two items of the stack, and push the result, this gives

```

 -----
 |   |
 |   |
 | 5 |
 -----
```

Finally RETURN_VALUE says to return the top item in the stack. In this case that item is 5, the result of a + b

The advantage with the bytecode and stack, is that anything that can hold a stack, and execute all of the bytecode instructions, can run Python. The goal of MCAlloy is to do this in Minecraft

With some of the new commands released in 1.13 and 1.14, it is possible to manipuate NBT data to simulate a stack, and with datapacks, it is possible to execute most of the bytecode commands in Python, all the is needed is to implement the bytecode commands.

There are some snags to this, first is there are 119 bytecode instructions in python 3.7. But if compiling without optimization, and ignoring instructions tht are impossible to implement like async calls, we are left with only 20-30 which is more reasonable. 
Most of those instructions are straightforward, but a handful of them do not translate well to Minecraft and will have to be dealt with creatively.

Each of these problems, and their solutions are explained in more detail in the pipeline.

### The Stack

Similarly to Python, MCAlloy's execution is done on a stack. This stack exists in the NBT data of pieces of paper held by invisible armor stands. The NBT of the armor stand looks something like:
```
{
    Tags: [".dest", ".volatile"],
    UUIDMost: 0L, UUIDLeast: <id>L,
    ArmorItems: [
        {
            id: "minecraft:paper", Count: 1b, tag: {
                Stack: [{}, {}, {}],
                Consts: [],
                Names: {}
            }
        },
        {},
        {},
        {}
    ]
}
```

For some reason, in Minecraft the "tag" section of an item has no restriction on the structure of the data, anywhere else and data my not be stored correctly.

All values are stored in the format of `{v: <value>, t: <type>}` so the number 3 is stored as `{v: 3, t: "int"}`, and a car object could be stored as `{v:{wheel_count: {v: 4, t: "int"}, color: {v: "red", t: "str"}}, t: "car"}`

There may be many stacks existing simultaneously. For example, when calling a function, the caller creates an entirely new stack, copies over the necessary data, and then tells that ew stack to execute the called function. Afterwards, the caller copies the result of the function, and then kills the new stack.

It's worth noting that with very few exceptions, all NBT manipulations are done on @s because selectors such as @e are slower with many entities in the world. So in normal execution, the stack is executing it's own commands.  


### Execution

Normally, Python is executed by reading one bytecode instruction at a time, and carrying out the specific instruction on the stack. This is not possible to do efficiently in Minecraft, so we have to compile the bytecode into commands, and put them in a datapack.  


## PIPELINE

A high level overview of the compilation process goes something like this

1. Parse the Python code using the ast module to get the abstract syntax tree (AST)
2. Convert the Python AST to an Alloy, compiling select segments of the tree to bytecode using the dis module
3. Compile the Alloy to Instructions
4. Convert Instructions to Minecraft commands and place commands in the proper file location


### 1: AST

Generating the AST is usually a tricky process for compilers, but Python is amazing and has a module that will generate an abstract syntax tree from any string containing Python code.
because of this, this step takes about two lines of code to implement, and there's not much to say about it.


### 2: Alloy

A large flaw with mcfunctions is that the entire function is executed sequentially, each command must run one after the other with few exceptions. Even if a command fails, all commands following will continue to run.

This is contrasted with a CPU, where instructions are passed one by one, and execution can jump to skip over code, repeat code, etc. This is not possible in mcfunctions at the moment

This leaves MCAlloy in an awkward place. It would be easiest to compile the AST to Python bytecode using the dis module, and then implement each of the bytecode instructions in Python. Alloy does this to the best of it's ability, but for a select few statements like while loops, function definitions, and returns, it will not work.

This is why MCAlloy generates an "Alloy", a blend of abstract syntax tree and bytecode. Shown below is a simple program and the Alloy generated 

```python
x = 5
if x == a:
    print(x)
 
print("DONE")
```

```
Body:
  Byte:
    Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval=5, argrepr='5', offset=0, starts_line=2, is_jump_target=False)
    Instruction(opname='STORE_NAME', opcode=90, arg=0, argval='x', argrepr='x', offset=2, starts_line=None, is_jump_target=False)
  If:
    Test:
      Byte:
        Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='x', argrepr='x', offset=0, starts_line=3, is_jump_target=False)
        Instruction(opname='LOAD_NAME', opcode=101, arg=1, argval='a', argrepr='a', offset=2, starts_line=None, is_jump_target=False)
        Instruction(opname='COMPARE_OP', opcode=107, arg=2, argval='==', argrepr='==', offset=4, starts_line=None, is_jump_target=False)
        Instruction(opname='POP_TOP', opcode=1, arg=None, argval=None, argrepr='', offset=6, starts_line=None, is_jump_target=False)
    True:
      Byte:
        Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='print', argrepr='print', offset=0, starts_line=4, is_jump_target=False)
        Instruction(opname='LOAD_NAME', opcode=101, arg=1, argval='x', argrepr='x', offset=2, starts_line=None, is_jump_target=False)
        Instruction(opname='CALL_FUNCTION', opcode=131, arg=1, argval=1, argrepr='', offset=4, starts_line=None, is_jump_target=False)
        Instruction(opname='POP_TOP', opcode=1, arg=None, argval=None, argrepr='', offset=6, starts_line=None, is_jump_target=False)
    False:
  
  Byte:
    Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='print', argrepr='print', offset=0, starts_line=6, is_jump_target=False)
    Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval='DONE', argrepr="'DONE'", offset=2, starts_line=None, is_jump_target=False)
    Instruction(opname='CALL_FUNCTION', opcode=131, arg=1, argval=1, argrepr='', offset=4, starts_line=None, is_jump_target=False)
    Instruction(opname='POP_TOP', opcode=1, arg=None, argval=None, argrepr='', offset=6, starts_line=None, is_jump_target=False)
```

To generate the Alloy, the AST has all simple computations, comparisons, and assignments converted to Python bytecode. But anything that effects the flow of the program remains unchanged.


### 3: Instructions

In MCAlloy, an instruction is an intermediate language (IL) for Minecraft. Below are a few common instructions

```
LCON LoadConst, loads a constant value onto the top of the stack
BIOP BinaryOp, pop the top two items of the stack, do some operation (+, -, *, /) and push the result pack onto the stack
CARG CopyArgs, copy all argument passed into a function to the new stack
```

The instructions are designed to be as close as possible to Python bytecode, `LCON` behaves the same as Python's `LOAD_CONST`. But there are some more specialized commands such as `ICTX` or InitContext, which summons an armor stand with very specific NBT data in it.

These Instructions are used in code to represent much more complex commands. `LCON`, when convert into a command has the format of `/data modify entity @s ArmorItems[0].tag.Stack[] set from entity @s ArmorItems[0].tag.Consts[]`. Loading constants is something that happens in many places in the code, so Alloy abstracts the implementation.
 
This also has the benefit of making it very easy to adapt MCAlloy to new versions of minecraft. If there came a faster way to load constants in the future, it would only have to be changed in one place to have the improvement take effect.

Described below is MCAlloy's process for taking an Alloy and converting it into a series of instructions and blocks

#### Datapack

The datapack assembler is the highest level of assembler in MCAlloy, it doesn't do much other than look at the target folder, and tell the namespace assembler to deal with each folder


#### Namespace

The namespace assembler takes each namespace and gathers data needed for each of the modules


#### Module

The module assembler is a bit more complex than the two above it. It takes the code in a given file and tells the frame assembler to assemble it, but in addition it also creates an additional launcher frame
 
The launcher frame will become an .mcfunction the summons a new stack, and executes the modules code on the stack. 
  

#### Frame

The frame assembler is far more complex than all the others. It has the task of taking an Alloy and converting it into a series of "blocks" which are essentially .mcfunction files. The generated code has to behave identically to the same source code running on a Python virtual machine.



#### Block

Blocks are individual .mcfunction files, a block is a sequence of instructions that will always execute in series. These blocks then link to each other to recreate things like if statements, for loops, etc.
 