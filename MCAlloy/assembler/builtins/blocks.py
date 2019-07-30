def embed(f):
    return f


@embed
def set_block(x, y, z, block):
    """
    Sets the block at (x, y, z) to the given type

    Performance Impact: 7
    :param x:
    :param y:
    :param z:
    :param block:
    :return:
    """
    '/summon minecraft:area_effect_cloud ~ ~ ~ {Tags:["__cursor__"]}'
    '/data modify set @e[tag=.cursor] Position.x from entity ArmorItems[0].tag.Names.x'
    '/data modify set @e[tag=.cursor] Position.y from entity ArmorItems[0].tag.Names.y'
    '/data modify set @e[tag=.cursor] Position.z from entity ArmorItems[0].tag.Names.z'
    '/blocks set ~ ~ ~ {}'.format(block)  # TODO nbt copy the id in?
    '/kill @[tag=__cursor__,limit=1]'


@embed
def get_block_name(x, y, z):
    """

    :param x:
    :param y:
    :param z:
    :return:
    """
    '/summon minecraft:area_effect_cloud ~ ~ ~ {Tags:["__cursor__"]}'
    '/data modify set @e[tag=.cursor] Position.x from entity ArmorItems[0].tag.Names.x'
    '/data modify set @e[tag=.cursor] Position.y from entity ArmorItems[0].tag.Names.y'
    '/data modify set @e[tag=.cursor] Position.z from entity ArmorItems[0].tag.Names.z'
    '/data get block ~ ~ ~ '
