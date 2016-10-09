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

sql_DATABASE = config.get('settings', "db_snow")
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

class UniDic(sql_Base):
    __tablename__ = 'UniDic'
    __table_args__ = (
        PrimaryKeyConstraint('ID'),
    )

    ID = Column('ID', CHAR(length=6))
    POS = Column('POS', VARCHAR(length=20))
    POS_s1 = Column('POS_s1', VARCHAR(length=40))
    POS_s2 = Column('POS_s2', VARCHAR(length=40))
    POS_s3 = Column('POS_s3', VARCHAR(length=40))
    Conj_type = Column('Conj_type', VARCHAR(length=40))
    Conj_form = Column('Conj_form', VARCHAR(length=40))
    org_kana = Column('org_kana', VARCHAR(length=40))
    org_kanji = Column('org_kanji', VARCHAR(length=40))
    lemma = Column('lemma', VARCHAR(length=40))
    reading = Column('reading', VARCHAR(length=40))
    org2_kanji = Column('org2_kanji', VARCHAR(length=40))
    org2_kana = Column('org2_kana', VARCHAR(length=40))
