from PySide6.QtGui import QValidator


class PortfolioNameValidator(QValidator):
    def validate(self, text: str, pos: int) -> QValidator.State:
        if len(text) < 1:
            return QValidator.State.Intermediate
        elif len(text) >= 30:
            return QValidator.State.Invalid
        else:
            return QValidator.State.Acceptable


class SecuritySymbolValidator(QValidator):
    def validate(self, text: str, pos: int) -> QValidator.State:
        if len(text) == 0:
            return QValidator.State.Intermediate
        elif len(text) >= 10:
            return QValidator.State.Invalid
        else:
            return QValidator.State.Acceptable

    def validate_uniquness(
        self, text: str, added_securities: list[str]
    ) -> QValidator.State:
        if text in added_securities:
            return QValidator.State.Invalid

        return QValidator.State.Acceptable
