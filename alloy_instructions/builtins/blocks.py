def embed(f):
    return f


@embed
def set_block(x, y, z, block):
    """
    Sets the block at (x, y, z) to the given type

    Performance Impact: 6
    :param x:
    :param y:
    :param z:
    :param block:
    :return:
    """
    '/summon minecraft:area_effect_cloud ~ ~ ~ {Tags:[".cursor"]}'
    '/data modify set @e[tag=.cursor] Position.x from entity ArmorItems[0].tag.Names.x'
    '/data modify set @e[tag=.cursor] Position.y from entity ArmorItems[0].tag.Names.y'
    '/data modify set @e[tag=.cursor] Position.z from entity ArmorItems[0].tag.Names.z'
    '/blocks set ~ ~ ~ {}'.format(block)  # TODO nbt copy the id in?
