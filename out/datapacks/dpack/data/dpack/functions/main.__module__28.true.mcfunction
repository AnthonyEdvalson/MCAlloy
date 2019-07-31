#           < dpack:main.__module__28.true >
# 29:             print(-4)
data modify entity @s ArmorItems[0].tag.Stack[3] set from entity @s ArmorItems[0].tag.Names.print
data modify entity @s ArmorItems[0].tag.Stack[4] set from entity @s ArmorItems[0].tag.Consts[2]
summon minecraft:armor_stand ~ ~1 ~ {Tags:["__dest__", "__volatile__"]},ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{Pre:[{},{}]}},{},{},{}]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[1] set from entity @s ArmorItems[0].tag.Stack[5]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[0] set from entity @s ArmorItems[0].tag.Stack[4]
data modify entity @s ArmorItems[0].tag.Stack[4] set from entity @e[tag=__ret__,limit=1] ArmorItems[0].tag.Stack[0]
kill @e[tag=__ret__,tag=__volatile__,limit=1]
#           </dpack:main.__module__28.true >
