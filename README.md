# Todoika

## How to run

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
python cli_ui.py
```
