from result import Ok


class ReturnResult:
    key = "return_result"

    @classmethod
    def process(cls, **input):
        if len(input) == 1:
            value = list(input.values())[0]
            return Ok(value)
        else:
            return Ok(input)
