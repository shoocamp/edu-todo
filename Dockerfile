FROM python:3.11

RUN mkdir "/app"
WORKDIR "/app"

COPY . .

RUN python3.11 -m pip install -r requirements.txt

CMD PYTHONPATH=$PYTHONPATH:${PWD}/src python src/todoika/cli_ui.py --config config.toml
