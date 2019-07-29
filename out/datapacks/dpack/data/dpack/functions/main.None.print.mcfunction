########################################## <dpack:main.None.print>
########################################## 2:     '/tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}'
execute store success score pass ..ASM run tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tellraw @a {\"nbt\":\"ArmorItems[0].tag.Names.x.v\",\"entity\":\"@s\"}"}]
########################################## </dpack:main.None.print>
execute store success score pass ..ASM run data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[0] set from entity @s ArmorItems[0].tag.Consts[0]"}]
execute store success score pass ..ASM run scoreboard players set ret ..ASM 1
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: scoreboard players set ret ..ASM 1"}]
execute store success score pass ..ASM run tag @s add .ret
                                                                                                                                                                                                        execute if score pass ..ASM matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s add .ret"}]
