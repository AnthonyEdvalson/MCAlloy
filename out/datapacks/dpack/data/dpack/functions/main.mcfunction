########################################## <dpack:main>
########################################## 1: def print(x):
########################################## 4: class Counter:
########################################## 12: increase = Counter()
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.Counter
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.Counter"}]
execute store success score pass ..ASM run summon minecraft:armor_stand ~ ~1 ~ {Tags:[".dest", ".volatile"],ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{}},{},{},{}]}
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: summon minecraft:armor_stand ~ ~1 ~ {Tags:[\".dest\", \".volatile\"],ArmorItems:[{id:\"minecraft:paper\",Count:1b,tag:{}},{},{},{}]}"}]
execute store success score pass ..ASM run data modify entity @e[tag=.dest,limit=1] ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @e[tag=.dest,limit=1] ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Stack[0]"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @e[tag=.ret,limit=1] ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @e[tag=.ret,limit=1] ArmorItems[0].tag.Stack[0]"}]
execute store success score pass ..ASM run kill @e[tag=.ret,tag=.volatile,limit=1]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: kill @e[tag=.ret,tag=.volatile,limit=1]"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Names.increase set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.increase set from entity @s ArmorItems[0].tag.Stack[0]"}]
########################################## 14: v = increase.increase(10)
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.increase
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.increase"}]
execute store success score pass ..ASM run execute store result score t0 ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v"}]
execute store success score pass ..ASM run execute as @e run execute if score @s ..addr = t0 ..ASM run tag @s add .deref
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute as @e run execute if score @s ..addr = t0 ..ASM run tag @s add .deref"}]
execute store success score pass ..ASM run data modify set @s ArmorItems[0].tag.Stack[0] from entity @e[tag=.deref,limit=1] ArmorItems[0].tag.Names.increase
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify set @s ArmorItems[0].tag.Stack[0] from entity @e[tag=.deref,limit=1] ArmorItems[0].tag.Names.increase"}]
execute store success score pass ..ASM run tag @e[tag=.deref,limit=1] remove .deref
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @e[tag=.deref,limit=1] remove .deref"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Consts[0]"}]
execute store success score pass ..ASM run summon minecraft:armor_stand ~ ~1 ~ {Tags:[".dest", ".volatile"],ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{}},{},{},{}]}
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: summon minecraft:armor_stand ~ ~1 ~ {Tags:[\".dest\", \".volatile\"],ArmorItems:[{id:\"minecraft:paper\",Count:1b,tag:{}},{},{},{}]}"}]
execute store success score pass ..ASM run data modify entity @e[tag=.dest,limit=1] ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Stack[1]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @e[tag=.dest,limit=1] ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Stack[1]"}]
execute store success score pass ..ASM run data modify entity @e[tag=.dest,limit=1] ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @e[tag=.dest,limit=1] ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Stack[0]"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @e[tag=.ret,limit=1] ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @e[tag=.ret,limit=1] ArmorItems[0].tag.Stack[0]"}]
execute store success score pass ..ASM run kill @e[tag=.ret,tag=.volatile,limit=1]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: kill @e[tag=.ret,tag=.volatile,limit=1]"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Names.v set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.v set from entity @s ArmorItems[0].tag.Stack[0]"}]
########################################## 16: if v == increase.count:
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.v"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Names.increase
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Names.increase"}]
execute store success score pass ..ASM run execute store result score t0 ..ASM run data get entity @s ArmorItems[0].tag.Stack[1].v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 ..ASM run data get entity @s ArmorItems[0].tag.Stack[1].v"}]
execute store success score pass ..ASM run execute as @e run execute if score @s ..addr = t0 ..ASM run tag @s add .deref
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute as @e run execute if score @s ..addr = t0 ..ASM run tag @s add .deref"}]
execute store success score pass ..ASM run data modify set @s ArmorItems[0].tag.Stack[1] from entity @e[tag=.deref,limit=1] ArmorItems[0].tag.Names.count
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify set @s ArmorItems[0].tag.Stack[1] from entity @e[tag=.deref,limit=1] ArmorItems[0].tag.Names.count"}]
execute store success score pass ..ASM run tag @e[tag=.deref,limit=1] remove .deref
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @e[tag=.deref,limit=1] remove .deref"}]
execute store success score pass ..ASM run execute store result score t1 ..ASM run data get entity @s ArmorItems[0].tag.Stack[1].v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t1 ..ASM run data get entity @s ArmorItems[0].tag.Stack[1].v"}]
execute store success score pass ..ASM run execute store result score t0 ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v"}]
execute store success score pass ..ASM run scoreboard players set t2 ..ASM 0
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players set t2 ..ASM 0"}]
execute store success score pass ..ASM run execute if score t0 ..ASM = t1 ..ASM run scoreboard players set t2 ..ASM 1
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score t0 ..ASM = t1 ..ASM run scoreboard players set t2 ..ASM 1"}]
execute store success score pass ..ASM run execute store result entity @s ArmorItems[0].tag.Stack[0].v int 1 run scoreboard players get t2 ..ASM
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result entity @s ArmorItems[0].tag.Stack[0].v int 1 run scoreboard players get t2 ..ASM"}]
########################################## 16: if v == increase.count:
execute store success score pass ..ASM run execute store result score test ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score test ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v"}]
execute store success score pass ..ASM run execute if score test ..ASM matches 1 run function dpack:main_16true
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score test ..ASM matches 1 run function dpack:main_16true"}]
execute store success score pass ..ASM run execute store result score test ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score test ..ASM run data get entity @s ArmorItems[0].tag.Stack[0].v"}]
execute store success score pass ..ASM run execute if score test ..ASM matches 0 run function dpack:main_16false
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score test ..ASM matches 0 run function dpack:main_16false"}]
########################################## </dpack:main>
execute store success score pass ..ASM run execute if score ret ..ASM matches 0 run function dpack:main_16cont
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score ret ..ASM matches 0 run function dpack:main_16cont"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]"}]
execute store success score pass ..ASM run scoreboard players set ret ..ASM 1
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players set ret ..ASM 1"}]
execute store success score pass ..ASM run tag @s add .ret
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s add .ret"}]
