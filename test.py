from random import randint
from time import sleep

import pandas as pd

from database import models
from database.database import Database
import spacy

# orm_database = Database("postgresql://postgres:@192.168.1.11/test")
orm_database = Database("sqlite:///database.sqlite")

article_ids = orm_database.get_article_ids()
for el in article_ids:
    test = orm_database.get_not_translated_sentences_df(el)
    test.to_excel(f"{el}.xlsx")
    print(1)
