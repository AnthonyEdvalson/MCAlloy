###########################################  < body >
########################################### 6:     def __init__(self):
########################################### - LNBT, TOS, {v: 1, t: "fptr"}
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag.Stack[-1] set from value {v: 1, t: "fptr"}
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag.Stack[-1] set from value {v: 1, t: \"fptr\"}"}]
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> LNBT "},{"text":"    "},{"text":"[0]"},{"text":"    "},{"text":"{v: 1, t: \"fptr\"}"}]execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"},{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}]
########################################### - SNAM, Counter.__init__, TOS
execute store success score pass __asm__ run data modify entity @s Counter.__init__ set from entity @s ArmorItems[0].tag.Stack[0]
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s Counter.__init__ set from entity @s ArmorItems[0].tag.Stack[0]"}]
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> SNAM "},{"text":"    "},{"text":"Counter.__init__"},{"text":"    "},{"text":"[-1]"}]execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"},{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}]
###########################################  </body >
###########################################  < links >
###########################################  </links >
