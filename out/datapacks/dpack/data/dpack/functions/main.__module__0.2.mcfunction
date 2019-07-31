#   < dpack:main.__module__0.2 >
# 36: print(a + b)
data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Names.print
data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.a
data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Names.b
execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[2].v
execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v
scoreboard players operation t0 __asm__ += t1 __asm__
execute store result entity @s ArmorItems[0].tag.Stack[1].v int 1 run scoreboard players get t0 __asm__
summon minecraft:armor_stand ~ ~1 ~ {Tags:["__dest__", "__volatile__"]},ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{Pre:[{},{}]}},{},{},{}]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[1] set from entity @s ArmorItems[0].tag.Stack[1]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[0] set from entity @s ArmorItems[0].tag.Stack[0]
data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @e[tag=__ret__,limit=1] ArmorItems[0].tag.Stack[0]
kill @e[tag=__ret__,tag=__volatile__,limit=1]
# 72: """
data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Consts[0]
data modify entity @s ArmorItems[0].tag.Names.__doc__ set from entity @s ArmorItems[0].tag.Stack[0]
#   </dpack:main.__module__0.2 >
