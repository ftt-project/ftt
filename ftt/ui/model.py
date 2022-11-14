model = None


def get_model():
    global model
    if model is None:
        model = ApplicationModel()
    return model


class ApplicationModel:
    def __init__(self):
        self._portfolio_version_id = None
        self._portfolio_id = None

    @property
    def portfolio_id(self):
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value):
        self._portfolio_id = value

    @property
    def portfolio_version_id(self):
        return self._portfolio_version_id

    @portfolio_version_id.setter
    def portfolio_version_id(self, value):
        self._portfolio_version_id = value

    def __repr__(self):
        return f"ApplicationModel(portfolio_id={self.portfolio_id}, portfolio_version_id={self.portfolio_version_id})"

    def __str__(self):
        return self.__repr__()
