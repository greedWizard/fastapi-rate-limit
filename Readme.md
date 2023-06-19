## ТЗ

На любом Python веб-фреймворке реализовать следующую логику:

1. Создать модель User
2. Создать модель API-ключ для User'а

Реализовать 2 енпоинта:
* Ендпоинт № 1 должен создавать пользователя и API-ключ для него
* Ендпоинт № 2 должен возвращать количество запросов пользователя на данный ендпоинт № 2.

Пример структуры ответа:
 
```
{
    "02.06.2023 16:00": {
        "200": 3,
        "429": 32
    },
    "02.06.2023 16:01": {
        "200": 3,
        "429": 32,
	    "418": 1
    },
}
```

Формат ответа на ваше усмотрение. Главное вернуть время и кол-во успешных ответов и кол-во ответов с 429, 418 статусом.

Как вы уже догадались, нужно реализовать Rate limit по API-ключу на ваше усмотрение. Решение должно быть легко переиспользуемым для любых других ендпоинтов. Также должна быть возможность на каждый ендпоинт задавать уникальный лимит.

Количество запросов в единицу времени на ваше усмотрение. Главное, что Rate limit должен в случае "мощного ддоса" банить API-ключ на N минут. Следующие N минут ендпоинт возвращает статус 418.

Предполагается, что данный ендпоинт может сильно "разбухнуть", т.к. пользователи делают очень много запросов.
Подумайте над оптимизацией: временной диапазон в GET параметрах, кеш, индексы и т.п. на ваше усмотрение

Решение можете выложить к себе на гитхаб/гитлаб и прислать ссылку. Либо любым другим удобным способом.


## Запуск

Заполнить энвы по аналогии с ```.env.example```

### Через докер:

* ```make all``` - поднять приложение целиком
* ```make logs``` - смотреть логи
* ```make drop-all``` - остановить контейнеры

### Локально:

* ```poetry shell && uvicorn --factory api.app:create_app --host 0.0.0.0 --port 8000 --reload```

### Тесты
* ```pytest```


## TODO:
* Больше покрытия тестами
* Убрать ворнинги от алхимии (видимо неправильно закрывается сессия в случае ошибок http)
* можно отрефакторить, чтобы сделать зависимость ещё меньше
* UoW
