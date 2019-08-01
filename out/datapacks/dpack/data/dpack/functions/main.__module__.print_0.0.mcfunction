###########################################  < body >
########################################### 3:     '/tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}'
########################################### - /, tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}
                                                                                                                                                                                                        execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> /    "},{"text":"    "},{"text":"tellraw @a {\"nbt\":\"ArmorItems[0].tag.Names.x.v\",\"entity\":\"@s\"}"}]execute if entity @a[scores={__DEBUG__=1..}] run tellraw @a ["",{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"},{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}]
execute store success score pass __asm__ run tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}
                                                                                                                                                                                                        execute if score pass __asm__ matches 0 run tellraw @a [{"text": " !!!!!!!! FAIL: tellraw @a {\"nbt\":\"ArmorItems[0].tag.Names.x.v\",\"entity\":\"@s\"}"}]
###########################################  </body >
###########################################  < links >
###########################################  </links >
