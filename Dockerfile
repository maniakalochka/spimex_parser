FROM python:3.13-slim

WORKDIR /src

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY .env alembic.ini run.sh pyproject.toml  /src/

ENV PYTHONPATH="/src"

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY src/ /src/

COPY run.sh /src/run.sh
RUN chmod +x /src/run.sh
ENTRYPOINT ["/src/run.sh"]

CMD ["python3", "main.py"]
