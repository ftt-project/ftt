from PySide6.QtCore import QEvent, QObject


class PortfolioEventsFilter(QObject):
    def __init__(self, widget):
        super().__init__(widget)

    def eventFilter(self, obj, event):
        if event.type() == RandomEvent.idType:
            print("RandomEvent: PortfolioVersionsChangedEvent")
            return True
        elif event.type() == PortfolioVersionsChangedEvent.idType:
            print("PortfolioVersionsChangedEvent: RandomEvent")
            return True
        else:
            print("Other event", event)
            return super().eventFilter(obj, event)


class PortfolioVersionsChangedEvent(QEvent):
    idType = QEvent.registerEventType()

    def __init__(self, portfolio_id):
        super().__init__(QEvent.Type(self.idType))

        self.portfolio_id = portfolio_id


class RandomEvent(QEvent):
    idType = QEvent.registerEventType()

    def __init__(self):
        super().__init__(QEvent.Type(self.idType))
