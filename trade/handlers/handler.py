class Handler:
    @classmethod
    def handle(cls, **kwargs):
        result = cls.handlers[0].process(**kwargs)
        for step in cls.handlers[1:]:
            if result.is_ok():
                result = step.process(**result.ok())
            else:
                break
        return result
