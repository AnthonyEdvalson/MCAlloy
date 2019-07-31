#   < dpack:main.__module__0.0 >
# 19: """
data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Consts[0]
data modify entity @s ArmorItems[0].tag.Names.__doc__ set from entity @s ArmorItems[0].tag.Stack[0]
# 21: if 1 == 2:
data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Consts[0]
data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[1]
execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v
execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v
scoreboard players set t2 __asm__ 0
execute if score t0 __asm__ = t1 __asm__ run scoreboard players set t2 __ASM__ 1
execute store result entity @s ArmorItems[0].tag.Stack[0].v int 1 run scoreboard players get t2 __ASM__
#   </dpack:main.__module__0.0 >
#   < Bridge if true: dpack:main.__module__21.true >
execute store result score test __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v
execute if score test __asm__ matches 1 run function dpack:main.__module__21.true
#   </Bridge if true: dpack:main.__module__21.true >
#   < Bridge if false: dpack:main.__module__21.false >
execute store result score test __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v
execute if score test __asm__ matches 0 run function dpack:main.__module__21.false
#   </Bridge if false: dpack:main.__module__21.false >
