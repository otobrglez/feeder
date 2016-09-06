from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from feeder.settings import DATABASE
from datetime import datetime
from sqlalchemy.dialects import postgresql
from psycopg2.extensions import register_adapter, AsIs, adapt
import arrow

from pdb import set_trace


def adapt_arrow(arrow_date):
    return AsIs("'%s'::timestamptz" % str(arrow_date))


def adapt_dict(some_dict):
    return AsIs("'oto'")


register_adapter(arrow.Arrow, adapt_arrow)
register_adapter(dict, adapt_dict)

Base = declarative_base()


def db_connect():
    return create_engine(URL(**DATABASE), echo=True)


class DBArticle(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    scraped_at = Column(DateTime(timezone=True), default=datetime.utcnow(), nullable=False)
    scraped_url = Column(Unicode(400), unique=True, nullable=False)
    domain = Column(Unicode(100), nullable=False)
    mobile_source_url = Column(Unicode(400), nullable=True)
    desktop_source_url = Column(Unicode(400), nullable=True)
    title_raw = Column(Unicode(400))
    title_clean = Column(Unicode(400), nullable=True)
    body_raw = Column(Text())
    body_clean = Column(Text(), nullable=True)
    date_at_raw = Column(DateTime(timezone=True), nullable=true)
    images = Column(postgresql.ARRAY(String))
    image_urls = Column(postgresql.ARRAY(String))
