# FTT

## Financial Trading Tools

> Finance is hard. Programming is hard.

FTT is a financial asset management application that helps to make right decision on time. 

## Main features

* Portfolio Building
* Assets Recommendation
* Portfolio testing
* Strategy testing
* Portfolio value tracking over the time
* Integration with Interactive Brokers
* Realtime signals trading decisions
* Web interface
* CLI interface

## Collaborators
- [Artem M](https://github.com/ignar)
- [Ihor M](https://github.com/IhorMok)


## Quickstart

```
pip install ftt
ftt bootstrap
ftt example
```


### Portfolio creation

*Import portfolio configuration from file*

```yaml
name: S&P companies
budget: 10000
symbols:
  - AAPL
  - MSFT
  - SHOP
period_start: 2020-01-01
period_end: 2021-01-01
interval: 5m
```

```
fft> portfolio import sp_companies.yml
```

*Create weights for portfolio*

```
ftt> portfolio build <ID>
```

## Development

Dependencies

* pyenv
* poetry

```commandline
pyenv install PYTHON_VERSION
pip install cmake
poetry update
```