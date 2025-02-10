from kafka import KafkaConsumer

from src.notification_service.telegram.settings import KafkaSettings
from src.notification_service.telegram.database.schemas import TelegramUserSchema
from src.notification_service.telegram.database.db_controller import TelegramUserController

topics = [KafkaSettings.topic_name_new_telegram_user, KafkaSettings.topic_name_delete_telegram_user]

with KafkaConsumer(
    *topics,
    bootstrap_servers=KafkaSettings.bootstrap_servers,
    auto_offset_reset="earliest",
    value_deserializer=lambda data: TelegramUserSchema.model_validate_json(data).model_dump()
) as consumer:
    for message in consumer:
        try:
            if message.topic == KafkaSettings.topic_name_new_telegram_user:
                TelegramUserController.create_or_update_user(message.value)
            elif message.topic == KafkaSettings.topic_name_delete_telegram_user:
                TelegramUserController.delete_user(message.value)
        except Exception as e:
            print(str(e))
            continue
