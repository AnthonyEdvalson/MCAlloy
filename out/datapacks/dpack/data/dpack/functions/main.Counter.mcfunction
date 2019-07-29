########################################## <dpack:main.Counter>
########################################## 5:     def __init__(self):
########################################## 8:     def increase(self, v):
########################################## </dpack:main.Counter>
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]"}]
execute store success score pass ..ASM run scoreboard players set ret ..ASM 1
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players set ret ..ASM 1"}]
execute store success score pass ..ASM run tag @s add .ret
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s add .ret"}]
