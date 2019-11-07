FROM python:3.7 AS base
WORKDIR /app
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config settings.virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev

FROM base AS dev
RUN poetry install

FROM base as prod
COPY src src
COPY alembic alembic
COPY wsgi.py alembic.ini app.py /app/
CMD gunicorn --workers 2 --worker-class sanic.worker.GunicornWorker --bind 0.0.0.0:80 wsgi
