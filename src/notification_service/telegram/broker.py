import json
import logging

from kafka import KafkaConsumer

from src.notification_service.telegram.settings import kafka_settings
from src.notification_service.telegram.database.schemas import TelegramUserSchema
from src.notification_service.telegram.database.db_controller import TelegramUserController

topics = [kafka_settings.topic_name_new_telegram_user, kafka_settings.topic_name_delete_telegram_user]


def get_data_from_msg(data: str) -> TelegramUserSchema:
    get_data = json.loads(data)
    return TelegramUserSchema.model_validate_json(get_data)


# Создание экземпляра KafkaConsumer
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=kafka_settings.bootstrap_servers,
    auto_offset_reset="earliest",
    value_deserializer=get_data_from_msg,
    sasl_mechanism="PLAIN",
    # sasl_plain_username=kafka_settings.kafka_username,
    # sasl_plain_password=kafka_settings.kafka_password,
    security_protocol='PLAINTEXT',
)

try:
    # Чтение сообщений
    for message in consumer:
        try:
            if message.topic == kafka_settings.topic_name_new_telegram_user:
                logging.debug(f"Создание нового пользователя: {message.value}")
                TelegramUserController.create_or_update_user(message.value)
            elif message.topic == kafka_settings.topic_name_delete_telegram_user:
                logging.debug(f"Удаление пользователя: {message.value}")
                TelegramUserController.delete_user(message.value)
        except Exception as e:
            logging.error(e)
            continue
finally:
    # Закрытие consumer при завершении работы
    consumer.close()
