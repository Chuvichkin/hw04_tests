# hw04_tests - Покрытие тестами, спринта 5 в Яндекс.Практикум
## Спринт 5 - Покрытие тестами


***

Задачи проекта:
* Для приложений posts и about написать всесторонние тесты. С их помощью убедиться, что всё работает как задумано.

***

Разворачивание проекта:

Клонировать репозиторий и перейти в его папку в командной строке:

```
git clone https://github.com/Chuvichkin/hw04_tests.git

cd hw04_tests
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

Для *nix-систем и MacOS:

```
source venv/bin/activate
```

Для windows-систем:

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
cd yatube
python3 manage.py migrate
```

Прогон тестов:
```
python3 manage.py test
```

***

## Автор проекта

Чувычкин Сергей.
