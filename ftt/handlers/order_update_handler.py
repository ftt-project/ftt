from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.order_steps.order_load_step import OrderLoadStep
from ftt.handlers.order_steps.order_update_step import OrderUpdateStep
from ftt.handlers.order_steps.order_weights_udpate_step import OrderWeightsUpdateStep


class OrderUpdateHandler(Handler):
    params = ("order_id", "dto")

    handlers = [
        (OrderLoadStep, "order_id"),
        (OrderUpdateStep, OrderLoadStep.key, "dto"),
        (OrderWeightsUpdateStep, OrderLoadStep.key, "dto"),
        (ReturnResult, OrderUpdateStep.key),
    ]
