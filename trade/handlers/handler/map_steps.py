from result import Ok


class MapSteps:
    def __new__(cls, next_step, prev_step):
        from_step_key, from_step_param = prev_step
        next_step_key, next_step_param = next_step

        class MapStepProcess:
            @classmethod
            def process(cls, **input):
                input[next_step_key][next_step_param] = input[from_step_key][
                    from_step_param
                ]
                return Ok(input)

        return MapStepProcess
