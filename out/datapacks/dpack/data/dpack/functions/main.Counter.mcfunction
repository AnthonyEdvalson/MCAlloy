########################################### - IFRM, 2
execute store success score pass __asm__ run tag @s remove __dest__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tag @s remove __dest__"}]
execute store success score pass __asm__ run data modify entity @s ArmorItems[0].tag set from value {Stack:[{},{}],Consts:[{v:"\"Counter\"", t:"<class 'str'>"},{},{v:"\"Counter.__init__\"", t:"<class 'str'>"},{},{v:"\"Counter.increase\"", t:"<class 'str'>"},{v:{}, t:"none"}],Names:{}}
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: data modify entity @s ArmorItems[0].tag set from value {Stack:[{},{}],Consts:[{v:\"\\\"Counter\\\"\", t:\"<class 'str'>\"},{},{v:\"\\\"Counter.__init__\\\"\", t:\"<class 'str'>\"},{},{v:\"\\\"Counter.increase\\\"\", t:\"<class 'str'>\"},{v:{}, t:\"none\"}],Names:{}}"}]
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> IFRM "},{"text":"    "},{"text":"2"}]execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"},{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}]
###########################################< body >
###########################################</body >
###########################################< links >
########################################### - BRGE, dpack:main.Counter_0.0
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> BRGE "},{"text":"    "},{"text":"dpack:main.Counter_0.0"}]
execute store success score pass __asm__ run execute if score ret __asm__ matches 0 run function dpack:main.Counter_0.0
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score ret __asm__ matches 0 run function dpack:main.Counter_0.0"}]
###########################################</links >
########################################### - RTRN, None
execute store success score pass __asm__ run execute if score ret __asm__ matches 0 run data modify entity @s ArmorItems[0].tag.Stack[-1] set from value {v:{}, t:"none"}
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score ret __asm__ matches 0 run data modify entity @s ArmorItems[0].tag.Stack[-1] set from value {v:{}, t:\"none\"}"}]
execute store success score pass __asm__ run execute if score ret __asm__ matches 0 run tag @s add __ret__
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score ret __asm__ matches 0 run tag @s add __ret__"}]
execute store success score pass __asm__ run execute if score ret __asm__ matches 0 run scoreboard players set ret __asm__ 1
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: execute if score ret __asm__ matches 0 run scoreboard players set ret __asm__ 1"}]
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> RTRN "},{"text":"    "},{"text":"None"}]
