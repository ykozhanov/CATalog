FROM python:3.13

WORKDIR /notification

RUN apt-get update && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/* \

COPY notification_service/pyproject.toml notification_service/
COPY notification_service/uv.lock notification_service/

COPY db_lib/pyproject.toml db_lib/
COPY db_lib/uv.lock db_lib/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync --directory notification_service/ --active
RUN uv sync --directory db_lib/ --active

ENV PYTHONPATH=/notification_service/:/notification_service/core/celery_config/
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

COPY supervisord.ini /etc/supervisor/conf.d/supervisord.ini
COPY notification_service/ notification_service/
COPY db_lib/ db_lib/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.ini"]
