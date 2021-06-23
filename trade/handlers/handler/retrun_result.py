class ReturnResult:
    def __init__(self, key):
        self.key = key

    def process(self, input):
        return input[self.key]
