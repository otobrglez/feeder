# -*- coding: utf-8 -*-
from feeder.models import *
from sqlalchemy.orm import sessionmaker

# from pdb import set_trace


class FeederPipeline(object):
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        repository = self.Session()

        if item.get('images'):
            item['images'] = [i['path'] for i in item.get('images')]

        article = DBArticle(**item)

        try:
            repository.add(article)
            repository.commit()
        except:
            repository.rollback()
            raise
        finally:
            repository.close()

        return item
