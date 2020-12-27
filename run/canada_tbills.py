import os
import fire
import pandas as pd

from trade.base_command import BaseCommand


class CanadaTbills(BaseCommand):
    def one_year_average(self):
        with open(os.path.join(os.getcwd(), "data", "tbill_all.csv"), "r") as csv_file:
            tbills = pd.read_csv(csv_file, header=0, index_col=0)
            average_2020 = tbills["2020-01-01":][["V80691346"]].mean(axis=0, skipna=True)
            average_2020 = average_2020["V80691346"]
            self.success(f"Average T-Bill (risk free) for 2020 is {average_2020}")

if __name__ == "__main__":
    fire.Fire(CanadaTbills)
