execute store success score pass __asm__ run tag @s remove __dest__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s remove __dest__"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Pre[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Pre[0]"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Names.self set from entity @s ArmorItems[0].tag.Pre[1]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.self set from entity @s ArmorItems[0].tag.Pre[1]"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Names.v set from entity @s ArmorItems[0].tag.Pre[2]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.v set from entity @s ArmorItems[0].tag.Pre[2]"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag set from value {Stack:[{},{},{}],Consts:[{}],Names:{}}
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag set from value {Stack:[{},{},{}],Consts:[{}],Names:{}}"}]
execute store success score pass __asm__ run function __callfunc__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: function __callfunc__"}]
############################################ <dpack:main.Counter.increase>
############################################ 9:         self.count += v
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.self
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.self"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Stack[0]"}]
execute store success score pass __asm__ run execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v"}]
execute store success score pass __asm__ run execute as @e run execute if score @s ..addr = t0 __asm__ run tag @s add __deref__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute as @e run execute if score @s ..addr = t0 __asm__ run tag @s add __deref__"}]
execute store success score pass __asm__ run data modify set @s ArmorItems[0].tag.Stack[1] from entity @e[tag=__deref__,limit=1] ArmorItems[0].tag.Names.count
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify set @s ArmorItems[0].tag.Stack[1] from entity @e[tag=__deref__,limit=1] ArmorItems[0].tag.Names.count"}]
execute store success score pass __asm__ run tag @e[tag=__deref__,limit=1] remove __deref__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @e[tag=__deref__,limit=1] remove __deref__"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @s ArmorItems[0].tag.Names.v
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @s ArmorItems[0].tag.Names.v"}]
execute store success score pass __asm__ run execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[2].v
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t1 __asm__ run data get entity @s ArmorItems[0].tag.Stack[2].v"}]
execute store success score pass __asm__ run execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v"}]
execute store success score pass __asm__ run scoreboard players operation t0 __asm__ += t1 __asm__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players operation t0 __asm__ += t1 __asm__"}]
execute store success score pass __asm__ run execute store result entity @s ArmorItems[0].tag.Stack[1].v int 1 run scoreboard players get t0 __asm__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result entity @s ArmorItems[0].tag.Stack[1].v int 1 run scoreboard players get t0 __asm__"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @s ArmorItems[0].tag.Stack[1]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[2] set from entity @s ArmorItems[0].tag.Stack[1]"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Stack[0]"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Stack[2]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Stack[2]"}]
execute store success score pass __asm__ run execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[1].v"}]
execute store success score pass __asm__ run execute as @e run execute if score @s ..addr = t0 __asm__ run tag @s add __deref__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute as @e run execute if score @s ..addr = t0 __asm__ run tag @s add __deref__"}]
execute store success score pass __asm__ run data modify @e[tag=__deref__,limit=1] ArmorItems[0].tag.Names.count from entity set @s ArmorItems[0].tag.Stack[1]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify @e[tag=__deref__,limit=1] ArmorItems[0].tag.Names.count from entity set @s ArmorItems[0].tag.Stack[1]"}]
execute store success score pass __asm__ run tag @e[tag=__deref__,limit=1] remove __deref__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @e[tag=__deref__,limit=1] remove __deref__"}]
############################################ 10:         return self.count
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.self
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Names.self"}]
execute store success score pass __asm__ run execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute store result score t0 __asm__ run data get entity @s ArmorItems[0].tag.Stack[0].v"}]
execute store success score pass __asm__ run execute as @e run execute if score @s ..addr = t0 __asm__ run tag @s add __deref__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute as @e run execute if score @s ..addr = t0 __asm__ run tag @s add __deref__"}]
execute store success score pass __asm__ run data modify set @s ArmorItems[0].tag.Stack[0] from entity @e[tag=__deref__,limit=1] ArmorItems[0].tag.Names.count
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify set @s ArmorItems[0].tag.Stack[0] from entity @e[tag=__deref__,limit=1] ArmorItems[0].tag.Names.count"}]
execute store success score pass __asm__ run tag @e[tag=__deref__,limit=1] remove __deref__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @e[tag=__deref__,limit=1] remove __deref__"}]
############################################ 10:         return self.count
execute store success score pass __asm__ run scoreboard players set ret __asm__ 1
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players set ret __asm__ 1"}]
execute store success score pass __asm__ run tag @s add __ret__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s add __ret__"}]
############################################ </dpack:main.Counter.increase>
execute store success score pass __asm__ run execute if score ret __asm__ matches 0 run function dpack:main.Counter.increase_10return
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score ret __asm__ matches 0 run function dpack:main.Counter.increase_10return"}]
