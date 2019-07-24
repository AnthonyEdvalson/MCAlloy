import sys

from alloy_instructions.generators.datapack import ILDatapackGenerator
from mcgen.generator import DatapackGenerator
import sys


class ParseException(Exception):
    pass


def comp(in_path, out_path, gs):
    dpack_il_gen = ILDatapackGenerator(in_path)
    namespaces = dpack_il_gen.assemble()

    dp_folder = "{}/datapacks/{}/".format(out_path, dpack_il_gen.name)

    dpack_gen = DatapackGenerator(gs)
    dpack_gen.generate(dp_folder, namespaces)


class GenerationSettings:
    def __init__(self, argv):
        self.debug = "DEBUG" in argv
        self.warn_fail = "NOFAIL" not in argv
        self.comment = "NOCOMMENT" not in argv


gs = GenerationSettings(sys.argv)

comp(sys.argv[1],
     sys.argv[2],
     gs)
