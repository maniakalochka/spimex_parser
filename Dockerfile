FROM python:3.13-slim

WORKDIR /src

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY alembic.ini run.sh pyproject.toml poetry.lock*  /src/

COPY src/ /src/

ENV PYTHONPATH="/src"

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi


RUN chmod +x run.sh; ./run.sh

CMD ["python3", "main.py"]
