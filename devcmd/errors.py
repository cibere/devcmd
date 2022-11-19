class InvalidArgument(Exception):
    def __init__(self, where: str, given: str):
        self.where = where
        self.given = given

        super().__init__(f"Invalid argument given in command {where}: '{given}'")
