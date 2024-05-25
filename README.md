# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

------

### Окружение:

    make init
    source .venv/bin/activate

Создать и заполнить env файлы

    cp .example.env local.env
    cp .example.env docker.env

### Запуск:

    make docker-run

### Запуск локально:

Предварительно прокинуть порты из контейнеров редиса, БД и ES:

    export $(cat local.env)
    make local-run