# E2E UI

End-to-end тесты проверки сценариев авторизации, выбора товара и оформления покупки товара на сайте https://www.saucedemo.com/.

### ⚡ Быстрый старт

Чтобы запустить тесты, необходимо:

1. Установить [Python 3.12](https://www.python.org/downloads/);
2. Скачать данный репозиторий в виде zip-архива, нажав на зелёную кнопку "< > Code", после чего "Download ZIP";
3. Распаковать содержимое архива. Открыть папку SeleniumTestTask-master;
4. Запустить командную строку, изменить текущую рабочую директорию на папку SeleniumTestTask-master;
5. Создать виртуальное окружение: `python -m venv ./venv/`

6. Активировать виртуальное окружение:

- Для Windows (PowerShell): `.\venv\Scripts\activate.ps1`
- Для Windows (Командная строка): `.\venv\Scripts\activate.bat`
- Для Linux: `source ./venv/bin/activate`

7. Установить требуемые библиотеки:

- Для Windows: `.\venv\Scripts\python.exe -m pip install -r requirements.txt`
- Для Linux: `pip install -r requirements.txt`

8. Запустить скрипт:

- Для Windows: `.\venv\Scripts\python.exe main.py`
- Для Linux: `python3 main.py`

9. По прохождении всех тестов в командной строке отобразится сообщение "Ran 4 tests in **.***s", под которым будет написано "OK"