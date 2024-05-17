import redis


def connect_to_redis(host='localhost', port=6379, db=0):
    """
    Функция для подключения к базе данных Redis.
    
    Аргументы:
    - host: хост Redis (по умолчанию 'localhost')
    - port: порт Redis (по умолчанию 6379)
    - db: номер базы данных Redis (по умолчанию 0)
    
    Возвращает объект подключения Redis.
    """
    try:
        r = redis.StrictRedis(host=host, port=port, db=db)
        print("Успешное подключение к Redis.")
        return r
    except Exception as e:
        print(f"Ошибка подключения к Redis: {e}")
        return None


def add_json_to_redis(key, json_data, db):
    """
    Функция для добавления содержимого JSON файла в Redis по ключу.

    Аргументы:
    - json_data: добавляемые json данные
    - key: ключ, по которому будет сохранено содержимое JSON в Redis
    - db: БД

    Возвращает True, если данные успешно добавлены в Redis, и False в противном случае.
    """
    try:
        db.set(key, str(json_data))
        print(f"Данные успешно добавлены в Redis по ключу {key}.")
        return True
    
    except Exception as e:
        print(f"Ошибка добавления данных в Redis: {e}")
        return False
    

def delete_from_redis(key, db):
    """
    Функция для удаления данных из Redis по ключу.

    Аргументы:
    - key: ключ, по которому данные будут удалены из Redis
    - db: БД

    Возвращает True, если данные успешно удалены из Redis, и False в противном случае.
    """
    try:
        result = db.delete(key)
        if result == 1:
            print(f"Данные из Redis по ключу {key} успешно удалены.")
            return True
        else:
             print("Ошибка удаления данных из Redis. По данному ключу нет данных")
             return False
    
    except Exception as e:
        print(f"Ошибка удаления данных из Redis: {e}")
        return False



if __name__ == "__main__":
    db = connect_to_redis()
    
    json_data = {
        "name": "John",
        "age": 30,
        "city": "New York",
        "grades": [85, 90, 88],
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345"
        }
    }

    key = 1
    add_json_to_redis(key, json_data, db)

    #delete_from_redis(key, db)



