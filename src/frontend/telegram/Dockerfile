FROM python:3.13

WORKDIR /telegram

RUN apt-get update && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/* \

COPY frontend/telegram/pyproject.toml frontend/telegram/
COPY frontend/telegram/uv.lock frontend/telegram/

COPY db_lib/pyproject.toml db_lib/
COPY db_lib/uv.lock db_lib/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"


RUN uv sync --directory frontend/telegram/ --active
RUN uv sync --directory db_lib/ --active

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

COPY frontend/telegram/ frontend/telegram/
COPY db_lib/ db_lib/

CMD ["python", "frontend/telegram/main.py"]
