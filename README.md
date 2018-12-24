# Шаблон

Шаблон создан на основе [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/).

Создаем виртуальное окружение:

    $ ~/anaconda3/bin/python3 -m venv .venv
    $ source .venv/bin/activate

Устанавливаем пакеты:

    $ (.venv) pip install -e .[dev]

Чтобы зафиксировать версии пакетов в окружении:

    $ (.venv) pip-compile

## Утилиты

Форматирование комментариев и описаний к функциям и классам можно генерировать с
помощью утилиты `pyment`.

    $ pyment file.py

---

- [python - Setuptools "development" Requirements - Stack Overflow](https://stackoverflow.com/questions/28509965/setuptools-development-requirements)
