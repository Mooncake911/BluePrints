import redis
import logging
from threading import Lock
from typing import Any, Optional

# logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(*args, **kwargs)
            return cls._instance

    def _initialize(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        Инициализирует подключение к базе данных Redis.
        Этот метод вызывается только один раз при первом создании экземпляра.

        Аргументы:
        - host: хост Redis (по умолчанию 'localhost')
        - port: порт Redis (по умолчанию 6379)
        - db: номер базы данных Redis (по умолчанию 0)
        """
        try:
            self.db = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
            logger.info("Успешное подключение к Redis.")
        except Exception as e:
            self.db = None
            logger.error(f"Ошибка подключения к Redis: {e}")

    def keys(self):
        return self.db.keys('*')

    def add(self, key: str, data: str) -> bool:
        """
        Метод для добавления содержимого JSON в Redis по ключу.

        Аргументы:
        - key: ключ, по которому будет сохранено содержимое JSON в Redis
        - data: данные для сохранения в формате JSON

        Возвращает True, если данные успешно добавлены в Redis, и False в противном случае.
        """

        if self.db:
            try:
                self.db.set(key, data)
                logger.info(f"Данные успешно добавлены в Redis по ключу {key}.")
                return True
            except Exception as e:
                logger.error(f"Ошибка добавления данных в Redis: {e}")
                return False
        else:
            logger.error("Нет подключения к Redis.")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Метод для получения данных из Redis по ключу.

        Аргументы:
        - key: ключ, по которому данные будут извлечены из Redis

        Возвращает данные в формате JSON, если они существуют, и None в противном случае.
        """
        if self.db:
            try:
                data = self.db.get(key)
                if data:
                    return data
                else:
                    logger.info(f"Данные по ключу {key} не найдены.")
                    return None
            except Exception as e:
                logger.error(f"Ошибка получения данных из Redis: {e}")
                return None
        else:
            logger.error("Нет подключения к Redis.")
            return None

    def delete(self, key: str) -> bool:
        """
        Метод для удаления данных из Redis по ключу.

        Аргументы:
        - key: ключ, по которому данные будут удалены из Redis

        Возвращает True, если данные успешно удалены из Redis, и False в противном случае.
        """
        if self.db:
            try:
                result = self.db.delete(key)
                if result == 1:
                    logger.info(f"Данные из Redis по ключу {key} успешно удалены.")
                    return True
                else:
                    logger.warning(f"Ошибка удаления данных из Redis. По данному ключу {key} нет данных.")
                    return False
            except Exception as e:
                logger.error(f"Ошибка удаления данных из Redis: {e}")
                return False
        else:
            logger.error("Нет подключения к Redis.")
            return False

    def close(self):
        self.db.flushdb()
        self.db.flushall()
        self.db.close()


redis_manager = RedisManager(host='localhost', port=6379, db=0)  # Redis Manager is common for all program
