###########################################  < body >
########################################### 64: """
########################################### - LOAD, TOS, <Consts[0]>
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Consts[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[-1] set from entity @s ArmorItems[0].tag.Consts[0]"}]
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> LOAD "},{"text":"    "},{"text":"[0]"},{"text":"    "},{"text":"<Consts[0]>"}]execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"},{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}]
########################################### - SNAM, <Names.__doc__>, TOS
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Names.__doc__ set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Names.__doc__ set from entity @s ArmorItems[0].tag.Stack[0]"}]
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> SNAM "},{"text":"    "},{"text":"<Names.__doc__>"},{"text":"    "},{"text":"[-1]"}]execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"},{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}]
###########################################  </body >
###########################################  < links >
###########################################  </links >
