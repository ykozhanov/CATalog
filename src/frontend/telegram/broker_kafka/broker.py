import json
from contextlib import contextmanager
from typing import Generator

from kafka import KafkaProducer

from src.frontend.telegram.settings import KAFKA_BOOTSTRAP_SERVERS


@contextmanager
def producer_kafka() -> Generator[KafkaProducer, None, None]:
    with KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda data: json.dumps(data).encode("utf-8"),
        ) as p:
        yield p
