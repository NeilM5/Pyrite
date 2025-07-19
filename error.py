class Error(Exception):
    def __init__(self, name, details):
        super().__init__(f"{name}: {details}")
        self.name = name
        self.details = details

    def __str__(self):
        return f"{self.name}: {self.details}"