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

For some reason, almost every nbt structure in Minecraft has restrictions on what fields can exist except the "tag" section of an item, so everything we do is stored in there

All values are stored in the format of `{v: <value>, t: <type>}` so the number 3 is stored as `{v: 3, t: "int"}`, and a car object could be stored as `{v:{wheel_count: {v: 4, t: "int"}, color: {v: "red", t: "str"}}, t: "car"}`

Unlike Python, there may be many stacks existing simultaneously. For example, when calling a function, the caller creates an entirely new stack, copies over the necessary data, and then tells that new stack to execute the called function. Afterwards, the caller copies the result of the function, and then kills the new stack.
The reason this is done, is because of scope, it prevents the names of an inner stack frame overwriting the outer, and makes recursion trivial.

It's worth noting that with very few exceptions, all NBT manipulations are done using @s because selectors such as @e are slower (@s is O(1) time, @e is O(n)). So in normal execution, the armor stand running the code is the one being modified.  


### Execution

Normally, Python is executed by running a program that reads individual bytes from a stream of data, and carrying out the corresponding instructions on the stack. This is not possible to do efficiently in Minecraft, so we have to compile the bytecode into commands, and put them in a datapack.  


## PIPELINE

### Alloy generation

In MCAlloy, an Alloy is the intermediate data structure that bridges many of the gaps between Python and mcfunctions

Shown below is some python code, the generated AST, and the Alloy generated from tht AST

```python
# test.py
x = 4
if x == 4:
    print("Yes")
x = 15
```

```
Module(
    body=[
        Assign(
            targets=[
                Name(id='x',  ctx=Store())
            ],
            value=Num(n=4)),
        If(
            test=Compare(
                left=Name(id='x', ctx=Load()), 
                ops=[Eq()], 
                comparators=[Num(n=4)]), 
            body=[
                Expr(
                    value=Call(
                        func=Name(id='print', ctx=Load()), 
                        args=[Str(s='Yes')], 
                        keywords=[]))
            ],
            orelse=[])
        Assign(
            targets=[
                Name(id='x',  ctx=Store())
            ],
            value=Num(n=15)),
    ])
```

```
None:
  dpack:boop:
    dpack:boop:
      Body:
        Byte:
          Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval=4, argrepr='4', offset=0, starts_line=2, is_jump_target=False)
          Instruction(opname='STORE_NAME', opcode=90, arg=0, argval='x', argrepr='x', offset=3, starts_line=None, is_jump_target=False)
        Byte:
          Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='x', argrepr='x', offset=0, starts_line=3, is_jump_target=False)
          Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval=4, argrepr='4', offset=3, starts_line=None, is_jump_target=False)
          Instruction(opname='COMPARE_OP', opcode=107, arg=2, argval='==', argrepr='==', offset=6, starts_line=None, is_jump_target=False)
        If:
          True: dpack:boop_3true
          False: dpack:boop_3false
          Continue: dpack:boop_3cont
      Bridge: dpack:boop_3cont
      Targets:
        dpack:boop_3cont:
          Body:
            Byte:
              Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval=15, argrepr='15', offset=0, starts_line=5, is_jump_target=False)
              Instruction(opname='STORE_NAME', opcode=90, arg=0, argval='x', argrepr='x', offset=3, starts_line=None, is_jump_target=False)
          Bridge: None
          Targets:
            dpack:boop_3true:
              Body:
                Byte:
                  Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='print', argrepr='print', offset=0, starts_line=4, is_jump_target=False)
                  Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval='Yes', argrepr="'Yes'", offset=3, starts_line=None, is_jump_target=False)
                  Instruction(opname='CALL_FUNCTION', opcode=131, arg=1, argval=1, argrepr='1 positional, 0 keyword pair', offset=6, starts_line=None, is_jump_target=False)
                  Instruction(opname='POP_TOP', opcode=1, arg=None, argval=None, argrepr='', offset=9, starts_line=None, is_jump_target=False)
              Bridge: None
              Targets:
            
            dpack:boop_3false:
              Body:
            
              Bridge: None
              Targets:
```

The Alloy is generated from an AST with the following rules

1. All stack frames are stored in a list inside the module, instead of being generated at runtime
2. All code within a frame is divided into a graph of blocks, each block must runs sequentially from start to finish. Branching execution is only possible by deciding which block executes once one finishes
3. All statements whose bytecode cleanly translates into minecraft commands will be converted into Byte notes

Rule 1 exists to make stack frames easier to handle, and simplify the process of making function calls later in the code.
Rule 2 exists because an mcfunction don't support if statements for large blocks of code without hurting performance. By dividing the flow fo the program into blocks now simplifies all future steps
Rule 3 exists because we can easily convert most bytecode to minecraft commands. By compiling those statements to bytecode now, we can treat `x = 15`, `func(15)`, and `x = (f(v.f(4) + 3) < y // 4)` identically. 
But statements like `def`, `for`, and `while`, must be handled in Minecraft a way that is fundamentally different than in Python

What primarily determines if a statement can be converted to a Byte node, is how it handles execution flow. Statements that always execute the same instructions in the same order
can most likely be converted to a Byte node. But loops and while cannot, since their flow isn't fixed  

It's worth noting that function calls are in Byte nodes. This is because after calling a function, execution continues normally.
Because the flow of execution is always the same, we can safely convert it to a Byte node.

The layout for the higher level structures looks like 

```
Module:
    Frame:
        Block:
            Body:
                ...
            Targets:
                Block:
                    Body:
                        ...
                    Targets:
                        ...
                Block:
                    ...
```

A Module is the highest level construct, it holds everything in a single .py file.

A Frame holds everything in a stack frame. There is one frame for the main body of the module, and additional ones for each function or class in the module

A Block holds a continuous series of instructions in its body. Blocks must always execute one after the next from start to finish.
In the previous example with a single if statement, there are 4 blocks:

 1. everything before the If, the test condition, and code to execute blocks 2 or 3 based on result.
 2. code to execute if the condition is true
 3. code to execute if the condition is false
 4. everything after the If. This block is bridged from the 1st, meaning that under normal execution, this block will run once the 1st is done

All blocks are stored in a hierarchy, with the first block to execute at the top stored inside a Frame

The purpose behind this particular structure is it translates well to mcfunctions. There is special code that needs to run For every frame and block, storing
the information for frames and blocks directly in the Alloy makes it much incredibly easy to deal with in the assembler. It also makes it trivial to split the code
into multiple mcfunction files, because each Block becomes exactly one file, and the list of targets tells how to chain them together. 

> Developer's note
>
> In early versions of MCAlloy, there wasn't an Alloy or any custom data structure passed to compiler, I was trying to compile by traversing Python's AST,
> Which ended up being too difficult, the code was hard to read and was quickly becoming spaghetti, and I was losing interest in the project. 
> I had thought about making an intermediate data structure for a while, but I kept putting it off because I'd have to start 
> all over on the core of the entire system, something that I had spent over a month on.
> But eventually I did it, I added Alloys, and rewrote everything around them. It probably saved the project. The code is simple, easy to understand
> and I'm happy with how it turned out. I guess the lesson here is don't be afraid to refactor, it often makes code easier to work with. And if it didn't,
> hopefully you remembered to make a backup

### Alloy Flow Structures

There are multiple ways to simulate statements like if and while with blocks. There are many ways to connect the blocks, each with benefits and drawbacks.
Below are listed 1 or 2 ways to represent each. To describe the blocks, a special notation is used.

`A -> B` Means that A can execute B if a condition is met (A targets B). A will resume once B is done
`A => B` Means that A is bridged to B, meaning once A is done, it will call B unless the return flag is set (A bridges to B)



#### If

Block Structure:

<Pre>
if:
    <True>
else:
    <False>
<Post>

Branching Flow:

Pre -> True  Pre -> False  True => Post  False => Post

After the condition in the if statement is evaluated, the Pre block decides to execute either the True or False block.
Once that block is done, they then bridge to Post. Execution never returns to Pre until the frame is returning

Returning Flow (Used in Alloy):

Pre -> True Pre -> False Pre => Post

After the if condition is evaluated the Pre bock executes either True or False, but True and False have no targets or bridges.
Because of this, once True or False ends, execution is returned to Pre, who then passes Postrol to Post

Branching flow feels more natural. Conceptually, execution is continued from the True and False blocks, so they should feed into the Post block directly
But there is a slight difference. Minecraft has to keep track of all the mcfunctions currently running, and in branching flow, we leave with Post executing and
both Pre and True/False on hold. In the latter case, only Pre is being held.

From this perspective, returning flow is slightly better, since it has less function calls accumulating. 

#### While

Block Structure:

<Pre>
while <Test>:
    <While>
<Post>

Winding Flow (Used in Alloy):

Pre => Test  Test => Post  Test -> While  While => Test

Returning Flow:

Pre -> Test  Pre => Post  Test -> While  While => Test

The comparison here is similar to the If. Winding flow is a slightly more naive approach, execution goes from Pre, to the Test. If the condition is true,
it executes While. While will always return execution to Test once done. This cucle repeats until the condition is false and Test does not execute While.
it then falls through to Post, and execution resumes.

The latter case is similar, but when the condition is false, Test stops completely and execution is resumed by Pre, who then bridges to Post.

The problem with winding flow is that Post is run with 2 functions on hold for each iteration. However it's simpler to code, since custom conditionals are only needed in
the Test block, in returning flow both Pre and Test need special code. This will be fixed in the near future so that while loops use returning flow to prevent
function accumulation

#### For



#### Return

Block Structure:

<Pre>
return
<Post>

Bridged Flow (Used by Alloy)

Pre => Post

Return Flow:



Return was included here for completion's sake. When returning, the program needs to stop executing. To do that we end the current block.
In bridged flow we have a bridge between the code before and after, in return flow we have no connection, and Post is ignored. Because of the return statement, all
bridges will be ignored, so both flow structures are basically the same. The reason alloy uses the first is because because by default, when a block is split
a bridge is made between them. So basically the first option is better because it's lazier  

##ASSEMBLING

Assembling is where the Alloy is converted into Blocks of instructions. An instruction represents a single action, such as putting a value on the stack,
storing the top value of the stack in a variable, creating an armor stand, etc. The AlloyCompiler converts an Alloy into Instructions by parsing each node
in the Alloy using the visitor pattern.

Below is a list of all nodes in an Alloy, and a brief description of the Instructions they generate

Module

Does not create any instructions, but does compile all frames within itself

Frame

Compiles the root block inside of it, and adds any needed frame initialization / destruction code

Block

Compiles everything within it's body, adds a `BlockBridge` instruction to the continuing block, and then assembles all target blocks

Byte

Compiles everything in it's bytecode to instructions, below are all supported Python bytecode operations

COMPARE_OP
BINARY_MULTIPLY BINARY_FLOOR_DIVIDE BINARY_MODULO BINARY_ADD BINARY_SUBTRACT
INPLACE_MULTIPLY INPLACE_FLOOR_DIVIDE INPLACE_MODULO INPLACE_ADD INPLACE_SUBTRACT
STORE_NAME LOAD_CONST LOAD_NAME LOAD_FAST STORE_ATTR LOAD_ATTR
CALL_FUNCTION RETURN_VALUE
ROT_TWO DUP_TOP POP_TOP

Of course this is not all Python opcodes, there are about 100 more that are not implemented by MCAlloy, but they are only used in either optimized code, 
in unsupported features like async calls, or they are only used in statements like If and For, which are never converted to bytecode.

If

It then adds two `CallBlockIf` instructions, one to execute the True block if the TOS is true, and one to execute the False if the TOS is false.
The TOS is then popped afterwards

While

The While node exists in the Test block

Return

Stops the current block, all remaining instructions in this block will not be compiled. A `Return` instruction is added that sets the ret flag to 1
During execution, when the ret flag is 1, all `BlockBridge` instructions will not continue execution. This flag is set back to 0 at the end of a frame. This system
ensures that code will never continue executing in a frame once a return statement is hit

FunctionDef / ClassDef

These nodes do nothing.





















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
 