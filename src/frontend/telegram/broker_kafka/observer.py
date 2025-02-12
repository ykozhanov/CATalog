from abc import ABC, abstractmethod
from cryptography.fernet import Fernet

from pydantic import BaseModel

from src.frontend.telegram.broker_kafka.schemas import TelegramUserSchema
from src.frontend.telegram.broker_kafka.broker import producer
from src.frontend.telegram.settings import KAFKA_TOPIC_ADD_NEW_USER, KAFKA_TOPIC_DELETE_USER, TOKEN_CRYPT_KEY


def encrypt_refresh_token(token: str) -> str:
    ciper = Fernet(TOKEN_CRYPT_KEY)
    return ciper.encrypt(token.encode("utf-8")).decode("utf-8")


class Observer(ABC):
    @abstractmethod
    def update(self, v: BaseModel):
        pass


class Subject(ABC):
    @abstractmethod
    def add_observer(self, o: Observer):
        pass

    @abstractmethod
    def delete_observer(self, o: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class KafkaUserObserver(Observer):
    def __init__(self, topic: str):
        self._topic = topic

    def update(self, v: TelegramUserSchema):
        producer.send(self._topic, dict(v))
        producer.flush()


class UserSubject(Subject):
    def __init__(self, user_id: int, chat_id: int, refresh_token: str | None = None):
        self._user = TelegramUserSchema(
            telegram_user_id=user_id,
            telegram_chat_id=chat_id,
            refresh_jtw_token=encrypt_refresh_token(refresh_token) if refresh_token is not None else refresh_token,
        )
        self._observers: list[Observer] = []

    def create_user(self):
        self.add_observer(KafkaUserObserver(KAFKA_TOPIC_ADD_NEW_USER))
        self.notify()

    def delete_user(self):
        self.add_observer(KafkaUserObserver(KAFKA_TOPIC_DELETE_USER))
        self.notify()

    def add_observer(self, o: Observer):
        self._observers.append(o)

    def delete_observer(self, o: Observer):
        self._observers.remove(o)

    def notify(self):
        for o in self._observers:
            o.update(self._user)
