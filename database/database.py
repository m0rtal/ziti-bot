import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models
from .models import Sentences, GazzettaArticle


class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url, pool_pre_ping=True)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def get_or_create(self, session, model, filter_field, data):
        instance = session.query(model).filter_by(**{filter_field: data[filter_field]}).first()
        if not instance:
            instance = model(**data)
        return instance

    def add_unique_record(self, data, model, filter_field):
        session = self.maker()
        article = self.get_or_create(session, model, filter_field, data)
        session.add(article)
        try:
            session.commit()
        except Exception as err:
            print(err)
            session.rollback()
        finally:
            session.close()

    def get_not_autotranslated_articles(self):
        session = self.maker()
        instance = session.query(GazzettaArticle).filter(
            models.GazzettaArticle.foreign_id.not_in(session.query(Sentences.foreign_id)))
        if not instance:
            return None
        return instance

    def get_article_ids(self):
        session = self.maker()
        model = models.GazzettaArticle
        instance = session.query(model.foreign_id).all()
        if not instance:
            return None
        return [el[0] for el in instance]

    def get_not_translated_sentences_df(self, filter_field):
        session = self.maker()
        query = session.query(Sentences).filter(Sentences.foreign_id == filter_field,
                                                Sentences.sentence_ru_valid == None)
        return pd.read_sql(query.statement, session.bind)
