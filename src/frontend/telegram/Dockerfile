FROM python:3.12.9

WORKDIR /telegram

COPY frontend/telegram/pyproject.toml src/frontend/telegram/
COPY frontend/telegram/uv.lock src/frontend/telegram/

COPY db_lib/pyproject.toml src/db_lib/
COPY db_lib/uv.lock src/db_lib/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN uv pip install src/frontend/telegram/ --system
RUN uv pip install src/db_lib/ --system

COPY frontend/telegram/ src/frontend/telegram/
COPY db_lib/ src/db_lib/

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV PYTHONPATH=/telegram/

CMD ["python", "-m" ,"src.frontend.telegram.main"]
