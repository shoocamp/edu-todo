FROM python:3.11

RUN mkdir "/app"
WORKDIR "/app"

COPY . /app
ENV PYTHONPATH=$PYTHONPATH:${PWD}/src

RUN python3.11 -m pip install -r requirements.txt

CMD python src/todoika/cli_ui.py --config config.toml
