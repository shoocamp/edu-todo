# Todoika

## How to run CLI UI

- Create and activate venv:

```bash
python3 -m vevn venv
source venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Init `sqlite` database:

```bash
sqlite3 todoika.db < scripts/init_db.sql
```

- Run CLI UI:

```bash
PYTHONPATH=$PYTHONPATH:${PWD}/src python src/todoika/cli_ui.py
```

## How to run tests

- Install dependencies:

```bash
pip install -r requirements_test.txt
```

- Run tests

```bash
pytest -vvv --cov-report term --cov=src
```
Сань я уже не помню шаги котоыре я делал пока настравиал постгрес(
помню что поставил 14 версию кажется.... больше ниечего не помню. все как-то сумбурно было.

ну и файл конфига я не стал пушать.

to install the connector library in a virtual environment

virtualenv env && source env/bin/activate
pip install psycopg2-binary

brew info postgresql
use postgresql@14 instead of deprecated postgresql
==> postgresql@14: stable 14.6 (bottled)
