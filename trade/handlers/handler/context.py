class Context:
    class Assigner:
        def __init__(self, assign, to):
            self.assign = assign
            self.to = to

        def process(self, context):
            context[self.to] = self.assign
            return context

    class Renamer:
        def __init__(self, rename, to):
            self.rename = rename
            self.to = to

        def process(self, context):
            context[self.to] = context[self.rename]
            del context[self.rename]
            return context

    def __new__(cls, **kwargs):
        if "assign" in kwargs:
            return Context.Assigner(**kwargs)
        elif "rename" in kwargs:
            return Context.Renamer(**kwargs)
        else:
            raise NotImplemented
