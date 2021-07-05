from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from trade.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep
from trade.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)
from trade.handlers.security_prices_steps.security_prices_upsert_step import (
    SecurityPricesUpsertStep,
)


class SecuritiesLoadingHandler(Handler):
    # TODO define handler input params and validate at the beginning
    # params = ("securities", "period_form, "period_to", "interval")
    #
    handlers = [
        (SecuritiesInfoDownloadStep, "securities"),
        (SecuritiesUpsertStep, SecuritiesInfoDownloadStep.key),
        (
            SecurityPricesDownloadStep,
            SecuritiesUpsertStep.key,
            "period_from",
            "period_to",
            "interval",
        ),
        (SecurityPricesUpsertStep, SecurityPricesDownloadStep.key, "interval"),
        ReturnResult(SecuritiesUpsertStep.key),
    ]
