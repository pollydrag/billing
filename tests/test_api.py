import pytest


@pytest.fixture
def billing_app(db):
    from billing import app
    return app.create_app()


async def test_create_client(aiohttp_client, billing_app):
    from billing.api import models

    client = await aiohttp_client(billing_app)

    response = await client.post(
        '/v1/clients',
        json={
            'login': 'test_login'
        }
    )

    assert response.status == 200, await response.text()
    response_json = await response.json()

    assert response_json == {
        'id': 1,
        'login': 'test_login'
    }

    db_clients = await billing_app.db.execute(
        models.clients.select()
    )
    assert dict(await db_clients.first()) == {
        'id': 1,
        'login': 'test_login',
    }

    db_wallets = await billing_app.db.execute(
        models.wallets.select()
    )
    assert dict(await db_wallets.first()) == {
        'id': 1,
        'client_id': 1,
        'currency': 'USD',
        'amount': 0,
    }


async def test_create_client_fail(aiohttp_client, billing_app):
    client = await aiohttp_client(billing_app)
    response = await client.post(
        '/v1/clients',
        json={'bad_request': ''}
    )
    assert response.status == 400, await response.text()


async def test_refill(aiohttp_client, billing_app):
    from billing.api import models

    client = await aiohttp_client(billing_app)

    await client.post(
        '/v1/clients',
        json={
            'login': 'test_login'
        }
    )

    response = await client.post(
        '/v1/wallets/refill',
        json={
            'client_id': 1,
            'amount': 10
        }
    )

    assert response.status == 200, await response.text()
    response_json = await response.json()
    assert response_json == {}

    db_wallets = await billing_app.db.execute(
        models.wallets.select()
    )
    assert dict(await db_wallets.first()) == {
        'id': 1,
        'client_id': 1,
        'currency': 'USD',
        'amount': 10,
    }


async def test_refill_fail(aiohttp_client, billing_app):
    client = await aiohttp_client(billing_app)
    response = await client.post(
        '/v1/wallets/refill',
        json={'bad_request': ''}
    )
    assert response.status == 400, await response.text()


async def test_transfer(aiohttp_client, billing_app):
    from billing.api import models

    client = await aiohttp_client(billing_app)

    await client.post(
        '/v1/clients',
        json={
            'login': 'src_client'
        }
    )

    await client.post(
        '/v1/clients',
        json={
            'login': 'dst_client'
        }
    )

    response = await client.post(
        '/v1/wallets/transfer',
        json={
            'src_client_id': 1,
            'dst_client_id': 2,
            'amount': 10
        }
    )

    assert response.status == 200, await response.text()
    response_json = await response.json()
    assert response_json == {}

    db_wallets = await billing_app.db.execute(
        models.wallets.select()
    )
    assert [dict(wallet) async for wallet in db_wallets] == [
        {
            'id': 1,
            'client_id': 1,
            'currency': 'USD',
            'amount': -10,
        },
        {
            'id': 2,
            'client_id': 2,
            'currency': 'USD',
            'amount': 10,
        }
    ]


async def test_transfer_fail(aiohttp_client, billing_app):
    client = await aiohttp_client(billing_app)
    response = await client.post(
        '/v1/wallets/transfer',
        json={'bad_request': ''}
    )
    assert response.status == 400, await response.text()
