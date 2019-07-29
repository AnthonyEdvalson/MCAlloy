############################################ <dpack:main.Counter.increase_10return>
############################################ </dpack:main.Counter.increase_10return>
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]"}]
execute store success score pass __asm__ run scoreboard players set ret __asm__ 1
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players set ret __asm__ 1"}]
execute store success score pass __asm__ run tag @s add __ret__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s add __ret__"}]
