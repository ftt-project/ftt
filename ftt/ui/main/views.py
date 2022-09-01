from PySide6.QtQuick import QQuickView


class MainView(QQuickView):
    def __init__(self, model):
        super().__init__()
        self.setResizeMode(QQuickView.SizeRootObjectToView)

        self.setInitialProperties({"myModel": model})

        self.setSource("ftt/ui/main/view.qml")
