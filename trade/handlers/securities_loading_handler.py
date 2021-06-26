from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.securities_steps.securities_load_info_step import SecuritiesLoadInfoStep
from trade.handlers.securities_steps.securities_load_prices_step import SecuritiesLoadPricesStep
from trade.handlers.security_prices_steps.security_prices_upsert_step import SecurityPricesUpsertStep
from trade.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep


class SecuritiesLoadingHandler(Handler):
    # TODO define handler input params and validate at the beginning
    # params = ("securities", "period_form, "period_to", "interval")
    #
    handlers = [
        (SecuritiesLoadInfoStep, "securities"),
        (SecuritiesUpsertStep, SecuritiesLoadInfoStep.key),
        (SecuritiesLoadPricesStep, SecuritiesUpsertStep.key, "period_from", "period_to", "interval"),
        (SecurityPricesUpsertStep, SecuritiesLoadPricesStep.key, "interval"),
        ReturnResult(SecuritiesUpsertStep.key)
    ]
