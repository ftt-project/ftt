from dataclasses import dataclass


@dataclass
class PortfolioNavigationEvent:
    """Event triggered by navigation buttons"""
    portfolio_id: str

    def __str__(self):
        return f"NavigationEvent: {self.portfolio_id}"


@dataclass
class PortfolioVersionBacktestingInitiateEvent:
    """Event triggered by backtesting button"""
    def __str__(self):
        return f"PortfolioVersionBacktestEvent"


@dataclass
class PortfolioBacktestPerformEvent:
    """Event that triggers backtesting"""
    version_ids: set[int]

    def __str__(self):
        return f"PortfolioBacktestPerformEvent"


class PortfolioVersionsDeselectedEvent:
    """Event triggered when no version is selected"""
    def __str__(self):
        return f"PortfolioVersionsDeselectedEvent"

@dataclass
class PortfolioSingleVersionSelectedEvent:
    """Event triggered by version selection"""
    version_id: int

    def __str__(self):
        return f"VersionSelectedEvent: {self.version_id}"


@dataclass
class PortfolioMultipleVersionsSelectedEvent:
    """Event triggered by multiple version selection"""
    version_ids: list

    def __str__(self):
        return f"VersionsSelectedEvent: {self.version_ids}"
