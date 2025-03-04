FROM python:3.12.9

WORKDIR /notification

RUN apt-get update && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY notification_service/pyproject.toml src/notification_service/
COPY notification_service/uv.lock src/notification_service/

COPY db_lib/pyproject.toml src/db_lib/
COPY db_lib/uv.lock src/db_lib/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN uv pip install src/notification_service/ --system
RUN uv pip install src/db_lib/ --system

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV PYTHONPATH=/notification/

COPY notification_service/supervisord.ini /etc/supervisor/conf.d/supervisord.ini
COPY notification_service/ src/notification_service/
COPY db_lib/ src/db_lib/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.ini"]
