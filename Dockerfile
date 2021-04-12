FROM python:3.9.2

WORKDIR /usr/src/app

COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install
