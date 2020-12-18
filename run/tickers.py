import fire
import os
import db.models as models
import db.configuration as configuration
import db.setup as dbsetup


class Tickers:
    """
    Tickers manipulations
    """

    def load(self):
        """
        Parses files from data folder and persist them using db.models.Ticker model
        """
        configuration.establish_connection()
        dbsetup.setup_database()

        for filename in os.listdir('./data'):
            with open(os.path.join(os.getcwd(), 'data', filename), 'r') as f:
                print(f"Processing {filename} file")
                lines = f.readlines()
                exchange = filename.split('.')[0]
                for line in lines:
                    line_data = line.split(maxsplit=1)
                    ticker = line_data[0].strip()
                    company_name = line_data[1].strip() if len(line_data) > 1 else None
                    models.Ticker.create(ticker=ticker, company_name=company_name, exchange=exchange)

        imported_records_count = models.Ticker.select().count()
        print(f"Import {imported_records_count} records")


if __name__ == '__main__':
  fire.Fire(Tickers)