import threading
import time

import fire
from ibapi.client import EClient

from pythonclient.ibapi.account_summary_tags import AccountSummaryTags
from pythonclient.ibapi.wrapper import EWrapper
from trade.base_command import BaseCommand


class AccountStatus(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        print("Acct# Summary. ReqId>:", reqId, "Acct:", account, "Tag: ", tag, "Value:", value, "Currency:", currency)

class Account(BaseCommand):
    def status(self):
        app = AccountStatus()
        app.connect('127.0.0.1', 7496, 0)
        t = threading.Thread(target=app.run)
        t.daemon = True
        t.start()
        time.sleep(1)

        app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)

        time.sleep(2)  # Sleep interval to allow time for incoming price data
        app.disconnect()

if __name__ == "__main__":
    fire.Fire(Account)