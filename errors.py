class InvalidTypeError(Exception):
    def __init__(self, target_type: str, source_type: str):
        self.source_type = source_type
        self.target_type = source_type
        super().__init__("Type mismatch expected {}, got {}".format(target_type, source_type))


class NotFoundError(Exception):
    pass
