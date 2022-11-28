from abc import ABCMeta

import pydantic
from result import Err, Ok
from typeguard import check_type

from ftt.handlers.handler.return_result import ReturnResult
from ftt.logger import Logger


class MetaHandler(ABCMeta):
    class HandlersAreMissing(Exception):
        pass

    class HandlerParamsAreMissing(Exception):
        pass

    def __new__(mcs, name, bases, dct):
        x = super().__new__(mcs, name, bases, dct)

        if x.__name__ != "Handler" and not hasattr(x, "handlers"):
            raise MetaHandler.HandlersAreMissing(f"{x} must define `handlers`")

        if x.__name__ != "Handler" and type(x.handlers) != list:
            raise ValueError(f"`{x}.handlers` must be type of list")

        if x.__name__ != "Handler" and not hasattr(x, "params"):
            raise MetaHandler.HandlerParamsAreMissing(f"{x} must define `params`")

        if x.__name__ != "Handler" and (
            type(x.params) != list and type(x.params) != tuple and type(x.params) != dict
        ):
            raise ValueError(f"`{x}.params` must be type of list, tuple, or dict")

        return x


class Handler(metaclass=MetaHandler):
    def __init__(self):
        self.context = {}

    def handle(self, **kwargs):
        normalized = self.__normalize_input(kwargs)

        self.context.update(normalized)
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
                Logger.error(f"ReturnResult is not set in context of {self.__class__}")
                return Err(last_result)

    def __normalize_input(self, input):
        if "model" in input.keys() and issubclass(type(input["model"]), pydantic.BaseModel):
            input_dict = input["model"].dict()
            input = {key: input_dict[key] for key in input_dict.keys() if key in self.__class__.params}

        if type(self.__class__.params) == tuple:
            difference = set(self.__class__.params).symmetric_difference(set(input.keys()))
            if len(difference) > 0:
                raise ValueError(
                    f"Given params {input.keys()} are not equal to required params. "
                    f"Difference {difference}"
                )
        elif type(self.__class__.params) == dict:
            for key, value in self.__class__.params.items():
                if key not in input.keys():
                    raise ValueError(f"Given params {input.keys()} are not equal to required params. Missing {key}")
                if check_type(input[key], input[key], value):
                    raise ValueError(f"Given params {input.keys()} are not equal to required params. {key} must be {value}")
        return input

    def __handle_processor(self, handle):
        if type(handle) is not tuple:
            return handle.process(self.context)

        step, *keys = handle
        args = {key: self.context.get(key) for key in keys}
        result = step.process(**args)
        self.context[step.key] = result.value
        return result
