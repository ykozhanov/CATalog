from kafka import KafkaConsumer

from src.notification_service.telegram.settings import kafka_settings
from src.notification_service.telegram.database.schemas import TelegramUserSchema
from src.notification_service.telegram.database.db_controller import TelegramUserController

topics = [kafka_settings.topic_name_new_telegram_user, kafka_settings.topic_name_delete_telegram_user]

# with KafkaConsumer(
#     *topics,
#     bootstrap_servers=kafka_settings.bootstrap_servers,
#     auto_offset_reset="earliest",
#     value_deserializer=lambda data: TelegramUserSchema.model_validate_json(data).model_dump(),
#     sasl_mechanism="PLAIN",
#     sasl_plain_username=kafka_settings.kafka_username,
#     sasl_plain_password=kafka_settings.kafka_password,
#     security_protocol='PLAINTEXT',
# ) as consumer:
#     for message in consumer:
#         try:
#             if message.topic == kafka_settings.topic_name_new_telegram_user:
#                 TelegramUserController.create_or_update_user(message.value)
#             elif message.topic == kafka_settings.topic_name_delete_telegram_user:
#                 TelegramUserController.delete_user(message.value)
#         except Exception as e:
#             print(str(e))
#             continue

# Создание экземпляра KafkaConsumer
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=kafka_settings.bootstrap_servers,
    auto_offset_reset="earliest",
    value_deserializer=lambda data: TelegramUserSchema.model_validate_json(data).model_dump(),
    sasl_mechanism="PLAIN",
    sasl_plain_username=kafka_settings.kafka_username,
    sasl_plain_password=kafka_settings.kafka_password,
    security_protocol='PLAINTEXT',
)

try:
    # Чтение сообщений
    for message in consumer:
        try:
            if message.topic == kafka_settings.topic_name_new_telegram_user:
                TelegramUserController.create_or_update_user(message.value)
            elif message.topic == kafka_settings.topic_name_delete_telegram_user:
                TelegramUserController.delete_user(message.value)
        except Exception as e:
            print(str(e))
            continue
finally:
    # Закрытие consumer при завершении работы
    consumer.close()
