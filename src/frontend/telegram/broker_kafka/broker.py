import json
from contextlib import contextmanager
from typing import Generator

from kafka import KafkaProducer

from src.frontend.telegram.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_USERNAME, KAFKA_PASSWORD


@contextmanager
def producer_kafka() -> Generator[KafkaProducer, None, None]:
    with KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda data: json.dumps(data).encode("utf-8"),
        sasl_mechanism="PLAIN",
        security_protocol='SASL_PLAINTEXT',
        sasl_plain_username=KAFKA_USERNAME,
        sasl_plain_password=KAFKA_PASSWORD,
        ) as p:
        yield p
