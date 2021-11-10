class Error(Exception):
    """Base class for other exceptions"""

    pass


class PersistingError(Error):
    """Exception raised for errors saving data to the database.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, model, params, message):
        self.model = model
        self.params = params
        self.message = message

    def __str__(self):
        return (
            f"Failed to persist `{str(self.model.__class__.__name__)}` "
            f"with params `{self.params}`. Failed with message: {self.message}"
        )
