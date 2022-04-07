from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_associate_empty_weights_step import (
    PortfolioVersionAssociateEmptyWeightsStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from ftt.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep
from ftt.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)
from ftt.handlers.security_prices_steps.security_prices_upsert_step import (
    SecurityPricesUpsertStep,
)


class PortfolioVersionSecuritiesAddingHandler(Handler):
    params = ("portfolio_version_id", "securities")

    # TODO rename to steps
    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (
            SecuritiesInfoDownloadStep,
            "securities",
        ),  # TODO rename to securities_symbols_list
        (SecuritiesUpsertStep, SecuritiesInfoDownloadStep.key),
        (
            SecurityPricesDownloadStep,  # TODO refactor to use PortfolioVersionDTO or PortfolioVersion
            SecuritiesUpsertStep.key,
            PortfolioVersionLoadStep.key,
        ),
        (
            SecurityPricesUpsertStep,
            SecurityPricesDownloadStep.key,
            PortfolioVersionLoadStep.key,
        ),
        (
            PortfolioVersionAssociateEmptyWeightsStep,
            "securities",
            "portfolio_version",
        ),
        (ReturnResult, PortfolioVersionLoadStep.key, SecuritiesUpsertStep.key),
    ]
