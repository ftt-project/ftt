Trade
=====

Why?
----
I want to have a passive income based on investing.

Installation
------------

Docker version

.. code:: bash
   docker build --tag trade:v[x] .
   docker run --rm -it --network host -v "$PWD:/usr/src/app" trade:v[x] run/account.py status

Create database & tables

.. code:: bash
    docker-compose --env-file .env.${ENV} up
    docker-compose run -e ENV_FILE=.env.${ENV} trade python ./bin/db.py create_database
    docker-compose run -e ENV_FILE=.env.${ENV} trade python ./bin/db.py create_tables

Run tests

.. code:: bash
    docker-compose run -e ENV_FILE=.env.test trade pytest test

Run Jupyter

.. code:: bash
    docker-compose run -e ENV_FILE=.env.dev -p 8888:8888 trade jupyter-lab --allow-root --ip=0.0.0.0

Plain code version

.. code:: bash

    pip install --upgrade pip
    pip install numpy
    pip install qdldl
    pip install osqp
    pip install cvxpy
    pip install cvxopt
    poetry install

Download all tickers
--------------------

.. code:: bash

    YahooTickerDownloader.py

Thought & ideas
---------------

Jan 7
^^^^^
- [ ] Was reading https://www.backtrader.com/docu/live/ib/ib/ and how to connect IB.
  The objective is to connect IB with backtrader and try it with SMA strategy
- [ ] Keep in mind how to manage existing portfolio with CPPI strategy

Mar 28
^^^^^^
- [ ] Rebuild portfolio for assets
- [ ] Rebuild portfolio for ETFs
- [ ] Buy using EB clients according to calculations
  - Save calculations
  - Buy on the breakthrought upright moment
- [ ] Monitor changes of each position and sell on peak
- [ ] Monitor changes of each position and sell on reaching a drawdown limit (CPPI)
- [x] Dockerize app
  - Jupyter image
  - Application image

Apr 11
^^^^^^
- [x] Docker composer with PG
- [x] Different PG environments for test and development

Apr 13
^^^^^^
- [x] Check run/tickers
- [x] Check run/history
- [ ] Use HistoryDataLoader service
- [ ] Calculate weights and save in DB
- [ ] Using calculated weights buy