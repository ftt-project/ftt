from tkinter import ttk

from ftt.ui.view import View


class NavigationView(View):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=600)

        self.label = ttk.Label(self, text="FTT")

    def post_initialize(self):
        self.label.grid(column=0, row=0)

    def navigation_clicked(self, portfolio_id):
        self.controller.navigation_clicked(portfolio_id)

    def add_portfolios(self, portfolios):
        for i, portfolio in enumerate(portfolios):
            button = ttk.Button(
                self,
                text=portfolio.name,
                command=lambda o=portfolio: self.navigation_clicked(o.id)
            )
            button.grid(column=0, row=i + 1)
