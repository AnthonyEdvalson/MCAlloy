#     < dpack:main.__module__33.test >
# 33: while 1 == 1:
data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Consts[0]
data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]
execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v
execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v
scoreboard players set t2 __asm__ 0
execute if score t0 __asm__ = t1 __asm__ run scoreboard players set t2 __ASM__ 1
execute store result entity @s ArmorItems[0].tag.Stack[0].v int 1 run scoreboard players get t2 __ASM__
#     </dpack:main.__module__33.test >
#     < Bridge if true: dpack:main.__module__33.while >
execute store result score test __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v
execute if score test __asm__ matches 1 run function dpack:main.__module__33.while
#     </Bridge if true: dpack:main.__module__33.while >
