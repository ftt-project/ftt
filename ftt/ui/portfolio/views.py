from tkinter import ttk, StringVar, NW

from ftt.ui.view import View


class PortfolioVersionWeightsView(View):
    def __init__(self, parent):
        super().__init__(parent)

        columns = (
            "position",
            "planned_position",
            "currency",
            "amount",
            "quote_type",
            "short_name",
        )

        self._treeview = ttk.Treeview(self, columns=columns)
        self._treeview.column('#0', width=100, anchor='center')
        self._treeview.heading('#0', text='Symbol')
        self._treeview.column('position', width=50, anchor='e')
        self._treeview.heading('position', text='Position')
        self._treeview.column('planned_position', width=100, anchor='e')
        self._treeview.heading('planned_position', text='Planned Position')
        self._treeview.column('currency', width=100, anchor='center')
        self._treeview.heading('currency', text='Currency')
        self._treeview.column('amount', width=100, anchor='e')
        self._treeview.heading('amount', text='Amount')
        self._treeview.column('quote_type', width=100, anchor='w')
        self._treeview.heading('quote_type', text='Quote Type')
        self._treeview.column('short_name', width=300, anchor='w')
        self._treeview.heading('short_name', text='Short name')

        self._treeview.grid(column=0, row=0)

    def post_initialize(self):
        pass

    def add_row(self, weight):
        self._treeview.insert("", "end", text=weight.security.symbol,
            iid=str(weight.id),
            values=(
                str(weight.position),
                str(weight.planned_position),
                weight.security.currency,
                str(weight.amount),
                weight.security.quote_type,
                weight.security.short_name,
            )
        )

    def remove_all_rows(self):
        self._treeview.delete(*self._treeview.get_children())


class PortfolioVersionsView(View):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=600)

        columns = (
            "active",
            "value",
            "period_from",
            "period_to",
            "interval",
            "annual_return",
            "annual_volatility",
            "sharpe_ratio",
        )

        self._treeview = ttk.Treeview(self, columns=columns)
        self._treeview.column('#0', width=100, anchor='center')
        self._treeview.heading('#0', text='Optimization Strategy')
        self._treeview.column('active', width=100, anchor='center')
        self._treeview.heading('active', text='Active')
        self._treeview.column('value', width=100, anchor='center')
        self._treeview.heading('value', text='Value')
        self._treeview.column('period_from', width=100, anchor='center')
        self._treeview.heading('period_from', text='Period From')
        self._treeview.column('period_to', width=100, anchor='center')
        self._treeview.heading('period_to', text='Period To')
        self._treeview.column('interval', width=100, anchor='center')
        self._treeview.heading('interval', text='Interval')
        self._treeview.column('annual_return', width=100, anchor='center')
        self._treeview.heading('annual_return', text='Annual Return')
        self._treeview.column('annual_volatility', width=100, anchor='center')
        self._treeview.heading('annual_volatility', text='Annual Volatility')
        self._treeview.column('sharpe_ratio', width=100, anchor='center')
        self._treeview.heading('sharpe_ratio', text='Sharpe Ratio')

        self._treeview.bind("<<TreeviewSelect>>", self.on_select_versions)

        self._treeview.grid(column=0, row=0)

    def post_initialize(self):
        pass

    def add_row(self, version):
        self._treeview.insert("", "end", text=str(version.optimization_strategy_name),
            iid=str(version.id),
            values=(
                "yes" if version.active else "no",
                version.value,
                version.period_start,
                version.period_end,
                version.interval,
                str(version.expected_annual_return),
                str(version.annual_volatility),
                str(version.sharpe_ratio),
            )
        )

    def remove_all_rows(self):
        self._treeview.delete(*self._treeview.get_children())

    def on_select_versions(self, _):
        items = self._treeview.selection()
        self.controller.on_select_version(items)


class PortfolioView(View):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=600)

        # self._versions_view = PortfolioVersionsView(self)
        # self._securities_view = PortfolioVersionWeightsView(self)
        self.label_var = StringVar()
        self.label = ttk.Label(self, textvariable=self.label_var)

    def post_initialize(self):
        # self._versions_view.controller = self.controller
        # self._versions_view.grid(column=0, row=1, sticky=NW)

        # self._securities_view.controller = self.controller
        # self._securities_view.grid(column=0, row=2, sticky=NW)

        self.label.grid(column=0, row=0)

    def show_portfolio(self, portfolio):
        self.label_var.set(portfolio.name)

    def show_active_version(self, portfolio_version):
        pass
