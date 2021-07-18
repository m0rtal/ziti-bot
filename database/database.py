from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models


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

    def add_record(self, data, model, filter_field):
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

    def get_article_by_foreign(self, filter_field):
        session = self.maker()
        model = models.GazzettaArticle
        instance = session.query(model).filter_by(foreign_id=filter_field).first()
        if not instance:
            return None
        return instance

