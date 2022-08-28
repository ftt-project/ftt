from ftt.ui.controller import Controller


class MainController(Controller):
    def initialize_and_render(self):
        self.view.grid(row=0, column=0)
        self.view.grid_rowconfigure(0, weight=1)
        self.view.grid_columnconfigure(0, weight=1)

    def update(self, event):
        pass
