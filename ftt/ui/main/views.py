from ftt.ui.view import View


class MainView(View):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def post_initialize(self):
        pass

    @property
    def controller(self):
        return None

    @controller.setter
    def controller(self, _):
        pass
