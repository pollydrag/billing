import aiopg.sa
import sqlalchemy as sa

metadata = sa.MetaData()

clients = sa.Table(
    'clients',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('login', sa.String)
)

wallets = sa.Table(
    'wallets',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('client_id', sa.Integer),
    sa.Column('currency', sa.String),
    sa.Column('amount', sa.DECIMAL)
)

history = sa.Table(
    'history',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('client_id', sa.Integer),
    sa.Column('amount', sa.DECIMAL)
)


async def get_client(db: aiopg.sa.SAConnection, client_id: int):
    result = await db.execute(
        clients.select().where(clients.c.id == client_id)
    )
    return dict(await result.first())


async def create_client(db: aiopg.sa.SAConnection, data):
    async with db.begin():
        result = await db.execute(clients.insert().values(**data))
        client_id = (await result.first()).id
        wallet = {
            'client_id': client_id,
            'currency': 'USD',
            'amount': 0,
        }
        await create_wallet(db, wallet)
    return client_id


async def create_wallet(db: aiopg.sa.SAConnection, data):
    result = await db.execute(wallets.insert().values(**data))
    return (await result.first()).id


async def refill_wallet(db: aiopg.sa.SAConnection, data):
    async with db.begin():
        await _change_balance(db, data['client_id'], data['amount'])


async def transfer(db: aiopg.sa.SAConnection, data):
    src = data['src_client_id']
    dst = data['dst_client_id']
    amount = data['amount']

    async with db.begin():
        await _change_balance(db, client_id=src, amount=(amount * -1))
        await _change_balance(db, client_id=dst, amount=amount)


async def _change_balance(db: aiopg.sa.SAConnection, client_id, amount):
    await db.execute(
        sa.update(wallets).values(
            amount=wallets.c.amount + amount).where(
            wallets.c.client_id == client_id)
    )
    await _add_to_history(db, client_id, amount)


async def _add_to_history(db: aiopg.sa.SAConnection, client_id, amount):
    await db.execute(
        history.insert().values(client_id=client_id, amount=amount)
    )
