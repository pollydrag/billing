import contextlib
import os
import time

import docker
import psycopg2
import pytest

import alembic.command
import alembic.config

DB_SETTINGS = {
    'dbname': 'billing',
    'user': 'postgres',
    'host': '127.0.0.1',
}


@pytest.fixture(scope='session')
def docker_client():
    return docker.from_env()


@pytest.fixture(scope='session')
def postgres_server(docker_client):
    cont = docker_client.containers.run(
        'postgres:12',
        detach=True,
        ports={'5432': '5432'},
        environment={
            'POSTGRES_DB': 'billing',
            'POSTGRES_HOST_AUTH_METHOD': 'trust'
        },
    )
    wait_for_postgres()
    yield
    cont.stop(timeout=1)


@pytest.fixture
def db(postgres_server):
    upgrade_db('head')
    yield
    downgrade_db('init')


def wait_for_postgres():
    while True:
        try:
            with contextlib.closing(psycopg2.connect(**DB_SETTINGS)) as conn:
               with conn.cursor() as cursor:
                   cursor.execute('select 1;')
                   break
        except psycopg2.Error:
            time.sleep(0.1)


alembic_cfg = alembic.config.Config(
    os.path.join(os.path.dirname(__file__), '../alembic.ini')
)


def upgrade_db(revision):
    alembic.command.upgrade(config=alembic_cfg, revision=revision)


def downgrade_db(revision):
    alembic.command.downgrade(config=alembic_cfg, revision=revision)
