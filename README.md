# Flight Tracking 

## Структура проекта: 
```
flight_tracker/
│
├── app.py                # Основной скрипт приложения
├── models.py             # Модели данных (SQLAlchemy)
├── data_loader.py        # Скрипт для загрузки данных в базу данных
├── config.py             # Конфигурационные параметры
├── requirements.txt      # Список зависимостей
├── README.md             # Описание проекта
└── reports.py
```

1. `app.py`
    - Основной скрипт приложения.
    - Получает данные о рейсах с [Flightradar24 API](https://www.flightradar24.com/airport/lcy).
    - Обрабатывает данные и сохраняет их в базу через SQLAlchemy.
2. `models.py `
    - Определяет структуру таблиц БД через классы  `Aircraft`, `Flight`.
3. `data_loader.py`
    - Содержит функции для добавления данных в БД (`add_aircraft`, `add_flight`).
    - Обрабатывает ошибки и транзакции
4. `config.py`
    - Хранит настройки подключения к БД (логин, пароль, хост).
5. `reports.py`
    - Генерирует отчеты PDF  и в консоле на основе данных из БД.
  
## Как запустить программу? 

Необходимо ввести в терминале следующие строки по очереди:

1. Cкачивание необходимых пакетов
```
pip install requirements.txt
```

2. Запуск программы
```
python app.py
```

3. Примерный вывод в терминале:
```
(.venv) PS C:\Users\Acer\Desktop\Repositories\Flight_Radar> python app.py
Данные успешно добавлены в таблицы!

Отладочная информация:
Самолеты: 15
Рейсы: 15

Daily Report: 
2025-04-07 22:00 | A321 | TK: 1 flights
2025-04-07 21:00 | A20N | PC: 3 flights
2025-04-07 21:00 | A21N | TK: 1 flights
2025-04-07 21:00 | A20N | U2: 1 flights
2025-04-07 21:00 | A21N | W9: 1 flights
2025-04-07 21:00 | B738 | XQ: 1 flights
2025-04-07 20:00 | B77W | TK: 1 flights
2025-04-07 20:00 | A21N | PC: 1 flights
2025-04-07 20:00 | B737 | 6H: 1 flights
2025-04-07 19:00 | A321 | TK: 1 flights
2025-04-07 19:00 | A21N | TK: 1 flights
2025-04-07 18:00 | A321 | TK: 1 flights
2025-04-07 18:00 | B738 | TK: 1 flights

Отчет также сохранен в PDF файл
(.venv) PS C:\Users\Acer\Desktop\Repositories\Flight_Radar> 
```

В данном случае отчет был сформирован по часам. Ниже прикрепляю фото бд: 
  
Пример того как выглядят таблицы в бд: 
(Я делала тесты с 10-15 самолетами для быстрой поверки работоспособности кода)

![image](https://github.com/user-attachments/assets/566e2c8f-6bba-45af-8df0-aee0d2fb8429)

![image](https://github.com/user-attachments/assets/d588234d-e381-4c49-8b9d-084a85c60568)


![image](https://github.com/user-attachments/assets/76e917a7-9b62-4ea9-b113-b131a76880c5)

