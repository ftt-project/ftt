from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
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


class SecuritiesInformationPricesLoadingHandler(Handler):
    params = ("securities", "portfolio_version")

    handlers = [
        (SecuritiesInfoDownloadStep, "securities"),
        (SecuritiesUpsertStep, SecuritiesInfoDownloadStep.key),
        (SecurityPricesDownloadStep, SecuritiesUpsertStep.key, "portfolio_version"),
        (SecurityPricesUpsertStep, SecurityPricesDownloadStep.key, "portfolio_version"),
        (ReturnResult, SecuritiesUpsertStep.key),
    ]
