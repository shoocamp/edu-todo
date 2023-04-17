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
- To re-init DB (run from root)
```bash
python scripts/psql_storage.py --config config.toml
```