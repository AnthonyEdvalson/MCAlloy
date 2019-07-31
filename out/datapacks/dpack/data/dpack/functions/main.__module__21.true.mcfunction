#     < dpack:main.__module__21.true >
# 22:     print(-2)
data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.print
data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Consts[2]
summon minecraft:armor_stand ~ ~1 ~ {Tags:["__dest__", "__volatile__"]},ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{Pre:[{},{}]}},{},{},{}]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[1] set from entity @s ArmorItems[0].tag.Stack[2]
data modify entity @e[tag=__dest__,limit=1] ArmorItems[0].tag.Pre[0] set from entity @s ArmorItems[0].tag.Stack[1]
data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @e[tag=__ret__,limit=1] ArmorItems[0].tag.Stack[0]
kill @e[tag=__ret__,tag=__volatile__,limit=1]
#     </dpack:main.__module__21.true >
