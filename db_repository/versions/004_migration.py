from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('location', String(length=50)),
    Column('date', DateTime),
    Column('description', String),
    Column('timestamp', DateTime, nullable=False, default=ColumnDefault(<function <lambda> at 0x034F70B0>)),
    Column('owner_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstname', String(length=100)),
    Column('lastname', String(length=100)),
    Column('email', String(length=120)),
    Column('pwdhash', String(length=54)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].drop()
    post_meta.tables['user'].drop()
