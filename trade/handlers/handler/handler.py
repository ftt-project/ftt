from result import Ok, Err


class Handler:
    def __init__(self):
        self.context = {}

    def handle(self, **input):
        self.context.update(input)
        for handle in self.__class__.handlers:
            if type(handle) == tuple:
                step, *keys = handle
                args = {key: self.context.get(key) for key in keys}
                result = step.process(**args)
                if result.is_ok():
                    self.context[step.key] = result.value
                else:
                    return Err(result)
            else:
                self.context = handle.process(self.context)
        return Ok(self.context)
