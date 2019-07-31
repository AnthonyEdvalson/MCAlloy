#       < dpack:main.__module__23.false >
# 26:     print(-4)
data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Names.print
data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @s ArmorItems[0].tag.Consts[2]
summon minecraft:armor_stand ~ ~1 ~ {Tags:["__dest__", "__volatile__"]},ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{Pre:[{},{}]}},{},{},{}]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[1] set from entity @s ArmorItems[0].tag.Stack[3]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[0] set from entity @s ArmorItems[0].tag.Stack[2]
data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @e[tag=__ret__,limit=1] ArmorItems[0].tag.Stack[0]
kill @e[tag=__ret__,tag=__volatile__,limit=1]
# 27:     if 2 == 2:
data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Consts[0]
data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @s ArmorItems[0].tag.Consts[0]
execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[3].v
execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[2].v
scoreboard players set t2 __asm__ 0
execute if score t0 __asm__ = t1 __asm__ run scoreboard players set t2 __ASM__ 1
execute store result entity @s ArmorItems[0].tag.Stack[2].v int 1 run scoreboard players get t2 __ASM__
#       </dpack:main.__module__23.false >
#       < Bridge if true: dpack:main.__module__27.true >
execute store result score test __asm__ run data get entity @s ArmorItems[0].tag.Stack[2].v
execute if score test __asm__ matches 1 run function dpack:main.__module__27.true
#       </Bridge if true: dpack:main.__module__27.true >
