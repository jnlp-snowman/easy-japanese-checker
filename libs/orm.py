# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine, orm
from sqlalchemy import CHAR, VARCHAR, Integer, Column, PrimaryKeyConstraint, ForeignKey
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('./config.ini')

sql_DATABASE = config.get('settings', "mysql")
sql_metadata = MetaData()
sql_engine = create_engine(
    sql_DATABASE,
    encoding='utf-8',
    pool_recycle=5,
)

db_session = orm.scoped_session(
    orm.sessionmaker(autocommit=True,
                    autoflush=True,
                    bind=sql_engine)
)

sql_Base = declarative_base()
sql_Base.query = db_session.query_property()

@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # optional - dispose the whole pool
        # instead of invalidating one at a time
        # connection_proxy._pool.dispose()

        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        raise exc.DisconnectionError()
    cursor.close()

class EasyUniDic(sql_Base):
    """
    """
    __tablename__ = 'easy_unidic'

    unidic_id = Column('unidic_id', VARCHAR(length=5), primary_key=True)
    surface = Column('surface', VARCHAR(length=50))

class EasyMorph(sql_Base):
    """
    """
    __tablename__ = 'easy_morph'

    id = Column('ID', VARCHAR(length=5), primary_key=True)
    org2_kanji = Column('org2_kanji', VARCHAR(length=40))


# class EasyUniDicView(sql_Base):
#     __tablename__ = 'easy_unidic_view'
#     unidic_id = Column('unidic_id', VARCHAR(length=5), primary_key=True)
#     surface = Column('surface', VARCHAR(length=50))
#     POS = Column('POS')
