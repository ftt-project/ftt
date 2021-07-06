from pygments.token import Token


class Prompt:
    def __new__(cls):
        return [
            (Token.String, "ftt"),
            (Token.Colon, ""),
            (Token.Pound, "> "),
        ]