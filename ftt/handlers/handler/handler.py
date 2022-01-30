from abc import ABCMeta

from result import Err, Ok

from ftt.handlers.handler.return_result import ReturnResult


class MetaHandler(ABCMeta):
    class HandlersAreMissing(Exception):
        pass

    class HandlerParamsAreMissing(Exception):
        pass

    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)

        if x.__name__ != "Handler" and not hasattr(x, "handlers"):
            raise MetaHandler.HandlersAreMissing(f"{x} must define `handlers`")

        if x.__name__ != "Handler" and type(x.handlers) != list:
            raise ValueError(f"`{x}.handlers` must be type of list")

        if x.__name__ != "Handler" and not hasattr(x, "params"):
            raise MetaHandler.HandlerParamsAreMissing(f"{x} must define `params`")

        if x.__name__ != "Handler" and (
            type(x.params) != list and type(x.params) != tuple
        ):
            raise ValueError(f"`{x}.params` must be type of list or tuple")

        return x


class Handler(metaclass=MetaHandler):
    def __init__(self):
        self.context = {}

    def handle(self, **input):
        self.__check_given_params(input)

        self.context.update(input)
        last_result = None
        for handle in self.__class__.handlers:
            last_result = self.__handle_processor(handle)
            if last_result.is_err():
                break

        if ReturnResult.key in self.context:
            return Ok(self.context[ReturnResult.key])
        else:
            if type(last_result) == Err:
                return last_result
            else:
                return Err(last_result)

    def __check_given_params(self, input):
        difference = set(self.__class__.params).symmetric_difference(set(input.keys()))
        if len(difference) > 0:
            raise ValueError(
                f"Given params {input.keys()} are not equal to required params. "
                f"Difference {difference}"
            )

    def __handle_processor(self, handle):
        if type(handle) is not tuple:
            return handle.process(self.context)

        step, *keys = handle
        args = {key: self.context.get(key) for key in keys}
        result = step.process(**args)
        self.context[step.key] = result.value
        return result
