from abc import ABCMeta

from result import Ok, Err


class MetaHandler(ABCMeta):
    class HandlersAreMissing(Exception):
        pass

    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)

        if x.__name__ != "Handler" and not hasattr(x, 'handlers'):
            raise MetaHandler.HandlersAreMissing(f"{x} must define `handlers`")

        if x.__name__ != "Handler" and type(x.handlers) != list:
            raise ValueError(f"`{x}.handlers` must be type of list")

        return x


class Handler(metaclass=MetaHandler):
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
