import json

from kafka import KafkaProducer

from src.frontend.telegram.settings import KAFKA_BOOTSTRAP_SERVERS

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda data: json.dumps(data).encode("utf-8"),
)
