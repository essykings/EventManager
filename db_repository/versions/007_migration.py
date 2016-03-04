from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=50)),
    Column('location', VARCHAR(length=50)),
    Column('date', DATETIME),
    Column('description', VARCHAR),
    Column('timestamp', DATETIME, nullable=False),
    Column('owner_id', INTEGER),
)

event = Table('event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('location', String(length=50)),
    Column('pic', LargeBinary),
    Column('date', DateTime),
    Column('description', String),
    Column('owner_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('firstname', VARCHAR(length=100)),
    Column('lastname', VARCHAR(length=100)),
    Column('email', VARCHAR(length=120)),
    Column('pwdhash', VARCHAR(length=54)),
    Column('pic', BLOB),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['timestamp'].drop()
    post_meta.tables['event'].columns['pic'].create()
    pre_meta.tables['user'].columns['pic'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['timestamp'].create()
    post_meta.tables['event'].columns['pic'].drop()
    pre_meta.tables['user'].columns['pic'].create()
