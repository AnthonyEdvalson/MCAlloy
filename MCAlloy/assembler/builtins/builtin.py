def print(x):
    """
    Prints the value of x to the chat

    Performance Impact: 1
    :param x: the value to print
    :return: None
    """
    '/tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.v","entity":"@s"}'
    '/tellraw @a {"nbt":"ArmorItems[0].tag.Names.x.s","entity":"@s"}'
    return None
