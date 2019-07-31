#           < dpack:main.__module__28.false >
# 31:             b += 2
data modify entity @s ArmorItems[0].tag.Stack[3] set from entity @s ArmorItems[0].tag.Names.b
data modify entity @s ArmorItems[0].tag.Stack[4] set from entity @s ArmorItems[0].tag.Consts[0]
execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[5].v
execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[4].v
scoreboard players operation t0 __asm__ += t1 __asm__
execute store result entity @s ArmorItems[0].tag.Stack[4].v int 1 run scoreboard players get t0 __asm__
data modify entity @s ArmorItems[0].tag.Names.b set from entity @s ArmorItems[0].tag.Stack[4]
#           </dpack:main.__module__28.false >
