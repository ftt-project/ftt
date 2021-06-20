from nubia import command


@command
def example():
    """
    Create example portfolio with weights
    1. create portfolio
    2. portfolio version
    3. load securities
    4. create weights
    5. calculate weights
    6. show portfolio stats
    """
    handler = PortfolioCreationHandler()
    result = handler.process(
        name='S&P companies',
        amount=10000
    )

