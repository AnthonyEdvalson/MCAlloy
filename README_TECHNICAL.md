# MCALLOY - TECHNICAL DETAILS

This document contains some details on the inner workings of MCAlloy, the information here isn't necessary to use MCAlloy.
if you are interested in how MCAlloy works, this contains a full overview of the system. The document is designed to be read by people who are familiar with Python, datapacks, compilers, and the Python virtual machine

## EXECUTION

Before looking in to the compilation, it is important to understand the method by which the code will execute in Minecraft, since that will shape the code's structure.

Python is a stack based language, all computation and execution is done in some way on a stack. For example, here is how Python interprets `a + b`

```
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```

This is Python bytecode, a series of instructs that will run on a stack.
 Lets assume a=2 and b=3. If the above code is executed, the value of "a" is loaded to the stack, abd then the value of "b". So after the first two instructions, the stack looks like

```

 -----
 | 3 |
 | 2 |
 -----
```

Then when BINARY_ADD is hit, the top two items of the stack will be removed, and their sum will be pushed, this gives

```

 -----
 |   |
 | 5 |
 -----
```

Finally RETURN_VALUE says to return the top item in the stack. In this case that item is 5, the result of a + b

The nice thing about Python's bytecode and stack, is that anything that can hold a stack, and execute all of the bytecode instructions, can run Python. The goal of MCAlloy is to do this in Minecraft

With some of the new commands released in 1.13 and 1.14, it is possible to manipulate NBT data to simulate a stack, and with datapacks, it is possible to execute most of the bytecode commands in Python.

There are some snags to this, first is there are 119 bytecode instructions in python 3.7. But if compiling without optimization, and ignoring instructions that are impossible to implement like async calls, we are left with only a few dozen. 
Most of those instructions are straightforward, but a handful of them do not translate well to Minecraft and will have to be dealt with creatively. Most of MCAlloy's code exists to deal with these special cases

Each of these problems, and their solutions are explained in more detail in the pipeline.

### The Stack

Similarly to Python, MCAlloy's execution is done on a stack. This stack exists in the NBT data of pieces of paper held by invisible armor stands. The NBT of the armor stand looks something like:
```
{
    Tags: ["__dest__", "__volatile__"],
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

For some reason, almost every nbt structure in Minecraft has restrictions on what fields can exist except the "tag" section of an item, so everything we do must be stored in there

All values are stored in the format of `{v: <value>, t: <type>}` so the number 3 is stored as `{v: 3, t: "int"}`, and a car object could be stored as `{v:{wheel_count: {v: 4, t: "int"}, color: {v: "red", t: "str"}}, t: "car"}`

Much like Python, MCAlloy almost never ever looks at types, except when using type() or isinstance()  

Unlike Python, there may be many stacks existing simultaneously. For example, when calling a function, the caller creates an entirely new stack, copies over the necessary data, and then tells that new stack to execute the called function. Afterwards, the caller copies the result of the function, and then kills the new stack.
The reason this is done, is because of scope, it prevents the names of an inner stack frame overwriting the outer, and makes recursion possible.

It's worth noting that with very few exceptions, all NBT manipulations are done on @s because selectors such as @e can be slow (@s is O(1) time, @e is O(n)). So in normal execution, the armor stand running the code is the one being modified.  


### Execution

Normally, Python is executed by running a program that reads individual bytes from a stream of data, and carrying out the corresponding instructions on the stack. This is not possible to do efficiently in Minecraft, so we have to compile the bytecode into commands, and put them in a datapack.  


## PIPELINE

### Alloy generation

In MCAlloy, an Alloy is the intermediate data structure that bridges many of the gaps between Python and mcfunctions

Shown below is some python code, the generated AST, and the Alloy generated from that AST

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

Rule 2 exists because an mcfunction can't have if statements for large blocks of code without hurting performance. By dividing the flow of the program into blocks, all future steps are made simpler

Rule 3 exists because we can easily convert most bytecode to minecraft commands. By compiling those statements to bytecode now, we can treat `x = 15`, `func(15)`, and `x = (f(v.f(4) + 3) < y // 4)` identically. 
But statements like `def`, `for`, and `while`, must be handled in Minecraft a way that is fundamentally different than in Python

What primarily determines if a statement can be converted to a Byte node, is how it handles execution flow. Statements that always execute the same instructions in the same order
can most likely be converted to a Byte node. But loops and whiles cannot, since their flow isn't fixed  

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

There are multiple ways to simulate statements like if and while with blocks. Each of the ways to connect the blocks has benefits and drawbacks.
Below are some of the simplest and best ways to represent various statements 

To describe the blocks, a special notation is used.

`A -> B` Target: Means that A can execute B if a condition is met. A will keep running once B is done

`A => B` Bridge: Means that A is bridged to B, meaning once A is done, it will call B unless the return flag is set



#### If

**Block Structure:**

```
<Pre>
if:
    <True>
else:
    <False>
<Post>
```
**Branching Flow:**

- Pre -> True
- Pre -> False
- True => Post
- False => Post

After the condition in the if statement is evaluated, the Pre block decides to execute either the True or False block.
Once that block is done, they then bridge to Post. Execution never returns to Pre until the frame returns

**Returning Flow** (Used in Alloy):

- Pre -> True
- Pre -> False
- Pre => Post

After the if condition is evaluated the Pre bock executes either True or False, but True and False have no targets or bridges.
So when True or False ends, execution is given back to Pre, who then bridges to Post

Branching flow feels more natural. Conceptually, execution is continued from the True and False blocks, so they should feed into the Post block directly
But there is a slight difference. Minecraft has to keep track of all the blocks currently running, and in branching flow, we leave with Post executing and
both Pre and True/False on hold. In the latter case, only Pre is being held.

From this perspective, returning flow is slightly better, since it has less function calls accumulating. 

#### While

**Block Structure:**
```
<Pre>
while <Test>:
    <While>
<Post>
```

**Winding Flow** (Used in Alloy):

- Pre => Test
- Test => Post
- Test -> While
- While => Test

**Returning Flow:**

- Pre -> Test
- Pre => Post
- Test -> While
- While => Test

The comparison here is similar to If. Winding flow is a slightly more naive approach, execution goes from Pre, to the Test. If the condition is true,
it executes While. While runs and then goes back to Test. This cycle repeats until the condition is false and Test does not execute While.
it then falls through to Post, and execution resumes.

The latter case is similar, but when the condition is false, Test stops completely and execution is resumed by Pre, who then bridges to Post.

The problem with winding flow is that Post is run with 2 mcfunctions on hold for each iteration. However it's simpler to code, since custom conditionals are only needed in
the Test block, in returning flow both Pre and Test need special code. This will be fixed in the near future so that while loops use returning flow to prevent
function accumulation

#### For

Not implemented yet

#### Return

**Block Structure:**
```
<Pre>
return
<Post>
```

**Bridged Flow** (Used by Alloy):

- Pre => Post

**Return Flow:**



Return was included here for completion's sake. When returning, the program needs to stop executing. To do that we end the current block.
In bridged flow we have a bridge between the code before and after, in return flow we have no connection, and Post is ignored. Because of the return statement, all
bridges will be ignored, so both flow structures are basically the same. The reason alloy uses the first is because because by default, when a block is ended
a bridge is made to the block containing the rest of the code. So basically the first option is better because it's lazier  

##ASSEMBLING

Assembling is where the Alloy is converted into Blocks of instructions. An instruction represents a single action, such as putting a value on the stack,
storing the top value of the stack in a variable, creating an armor stand, etc. The AlloyCompiler converts an Alloy into Instructions by parsing each node
in the Alloy using the visitor pattern.

Below is a list of all nodes in an Alloy, and a brief description of the Instructions they generate

**Module**

Does not create any instructions, only compiles all frames within itself

**Frame**

Compiles the root block inside of it, and adds any needed frame initialization / destruction code

**Block**

Compiles everything within it's body, adds a `BlockBridge` instruction to the continuing block, and then assembles all target blocks

**Byte**

Compiles everything in it's bytecode to MCAlloy's instructions, below are all supported Python bytecode operations, grouped by which instruction implements them

| Instruction | Bytecode Operations                                                                                                                                            |
|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| CompareOp   | COMPARE_OP          |
| BinaryOp    | BINARY_MULTIPLY BINARY_FLOOR_DIVIDE BINARY_MODULO BINARY_ADD BINARY_SUBTRACT INPLACE_MULTIPLY INPLACE_FLOOR_DIVIDE INPLACE_MODULO INPLACE_ADD INPLACE_SUBTRACT |
| Store       | STORE_NAME          |
| Load        | LOAD_NAME LOAD_FAST LOAD_CONST |
| StoreAttr   | STORE_ATTR          |
| LoadAttr    | LOAD_ATTR           |
|             | CALL_FUNCTION       |
| Return      | RETURN_VALUE        |
| Shuffle     | ROT_TWO ROT_THREE DUP_TOP DUP_TOP_TWO |
| Seek        | POP_TOP             |
 

**If**

It adds two `CallBlockIf` instructions, one to execute the True block if the TOS is true, and one to execute the False if the TOS is false.
The TOS is then popped afterwards

**While**

The While node exists in the Test block, it uses `CallBlockIf` to execute the while body if the TOS is true. Otherwise it does nothing

**Return**

Stops the current block, all remaining instructions in this block will not be compiled. A `Return` instruction is added that sets the ret flag to 1, and tags @s with \_\_ret\_\_
During execution, when the ret flag is 1, all `BlockBridge` instructions will not continue execution. This flag is set back to 0 at the end of a frame. This system
ensures that code will never continue executing in a frame once a return statement is hit

**FunctionDef / ClassDef**

These nodes do nothing.




## Function Context

A function context is an armor stand designed to execute mcfunctions. They go through the following steps to execute.

1. Caller runs `InitFunctionContext`, creating a new armor stand with the proper NBT scaffolding and tags
2. Caller stores fptr in a temporary scoreboard variable
3. Caller calls \_\_callfunc\_\_
4. \_\_callfunc\_\_ looks at temporary scoreboard variable, and selects the desired function based on value
5. \_\_callfunc\_\_ runs function on @e\[tag=\_\_dest\_\_\]
6. All functions begin by removing the \_\_dest\_\_ and initializing Stack and Consts
7. When the callee returns, the "ret" flag is set, and the context gains the \_\_ret\_\_ tag. The callee's stack should contain only the return value
8. Caller copies the bottom item of @e\[\_\_ret\_\_\]'s stack to it's own TOS
9. Caller kills @e\[tag=\_\_ret\_\_,tag=\_\_volatile\_\_\], which should include the callee, as long as the \_\_volatile\_\_ tag is present

For reference, the function context's NBT looks like this when created:

```
{
    Tags: ["__dest__", "__volatile__"],
    ArmorItems: [
        {
            id: "minecraft:paper", Count: 1b, tag: {
                Stack: [],
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

### Function Pointer (fptr)

Function pointers work similarly to function pointers in standard programming languages. They are a reference to a particular section of code.
During compilation, all functions are given a fptr which is an id. This id is just an arbitrary incrementing value that uniquely identifies a
function. This value is then used during execution to store a reference to that function. For example, a function `count()` with an id of 3 would
be stored as {v: 3, t: "func"} in NBT format.

the NBT data {v: 3, t: "func"} is enough to remember a function, but not enough to let us execute `count()`. \_\_callfunc\_\_ was created to bridge this gap

### \_\_callfunc\_\_

callfunc is a special function that is created once for all datapacks. Given a fptr, it will execute the associated function. It does this by a series
of function calls.

\_\_callfunc\_\_ is the "root" of a much larger tree of functions that conduct a binary search

```
# file: __callfunc__.0_3

execute if fptr __asm__ matches ..1 run function __callfunc__.0_1
execute if ret __asm__ matches 0 run function __callfunc__.2_3
``` 

The function name always \_\_callfunc\_\_ followed by the range of value being considered.
Inside the function is a single check that splits the range in half. If the fptr is in the upper half, it repeats the process with a upper half of the range, same with the lower half.
Eventually, the execution will reach a "Leaf" which looks like

```
# file: callfunc_.3_3

execute as @e[tag=__dest__,limit=1] run function datapack.module.count()
```

Once the binary search has found the target function, it executes it on the \_\_dest\_\_ function context.

Because this is a binary search, it runs slower depending on the number of functions. It takes an average of 3/2 * lg(n) commands to call 
a function in \_\_callfunc\_\_, where n is the total number of functions in the datapack. This isn't too bad but when considering the number of functions added by builtins 
and imports, it adds up quickly. With 128 functions, it is an average of 10.5 commands per function call. This overhead could become a problem if making many builtin
calls or using recursion.

Optimization can help a lot here. There are a few dozen builtins, most of which are never used. And when importing a module, it's rare that all of the available
functions are used. Optimization can scan through the code, and remove the functions that aren't being used. This has not been implemented yet in Alloy, although it
is a planned feature


### \_\_volatile\_\_ tag

The volatile tag is used whenever an object is made or destroyed. All created function contexts have the \_\_volatile\_\_ tag, and before destroying any
function contexts, the tag is checked for. This gives additional flexibility and security. The primary reason the tag exists is because the kill command
is devastating if it goes wrong. Players won't be happy if running any function in generated data pack with `/function` results in instant death. 
So as a rule, all entities in MCAlloy have to "elect" to be killable by adding the \_\_volatile\_\_ tag.
