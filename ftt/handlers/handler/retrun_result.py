from result import Ok


class ReturnResult:
    key = "return_result"

    @classmethod
    def process(cls, **input):
        value = list(input.values())[0]
        return Ok(value)
