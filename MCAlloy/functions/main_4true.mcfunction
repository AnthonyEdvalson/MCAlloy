########################################## <dpack:main_4true>
########################################## 5:         x = 2
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[1] set from entity @s ArmorItems[0].tag.Consts[0]"}]
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Names.x set from entity @s ArmorItems[0].tag.Stack[1]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.x set from entity @s ArmorItems[0].tag.Stack[1]"}]
########################################## </dpack:main_4true>
