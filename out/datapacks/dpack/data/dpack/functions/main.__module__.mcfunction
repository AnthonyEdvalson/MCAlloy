tag @s remove __dest__
data modify entity @s ArmorItems[0].tag.Names.__fptr__ set from entity @s ArmorItems[0].tag.Pre[0]
data modify entity @s ArmorItems[0].tag set from value {Stack:[{},{},{}],Consts:[{v:"\"\\ndef print(x):\\n    '/tellraw @a {\"nbt\":\"ArmorItems[0].tag.Names.x.v\",\"entity\":\"@s\"}'\\n\\nclass Counter:\\n    def __init__(self):\\n        self.count = 0\\n\\n    def increase(self, v):\\n        self.count += v\\n        return self.count\\n\\nincrease = Counter()\\n\\nv = increase.increase(10)\\n\\nif v == increase.count:\\n    print(increase.count)\\n\"", t:"<class 'str'>"},{v:1, t:"<class 'int'>"},{v:2, t:"<class 'int'>"},{v:3, t:"<class 'int'>"},{v:4, t:"<class 'int'>"},{v:{}, t:"none"},{v:-2, t:"<class 'int'>"},{v:-3, t:"<class 'int'>"},{v:-4, t:"<class 'int'>"},{v:-4, t:"<class 'int'>"}],Names:{}}
function __callfunc__
# < dpack:main.__module__ >
# </dpack:main.__module__ >
# < Bridge: dpack:main.__module__0.0 >
execute if score ret __asm__ matches 0 run function dpack:main.__module__0.0
# </Bridge: dpack:main.__module__0.0 >
# < Bridge: dpack:main.__module__0.1 >
execute if score ret __asm__ matches 0 run function dpack:main.__module__0.1
# </Bridge: dpack:main.__module__0.1 >
# < Bridge: dpack:main.__module__0.2 >
execute if score ret __asm__ matches 0 run function dpack:main.__module__0.2
# </Bridge: dpack:main.__module__0.2 >
execute if score ret __asm__ matches 0 run data modify entity @s ArmorItems[0].tag.Stack[-1] set from value {v:{}, t:"none"}
execute if score ret __asm__ matches 0 run tag @s add __ret__
execute if score ret __asm__ matches 0 run scoreboard players set ret __asm__ 1
