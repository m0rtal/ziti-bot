import os
from random import randint
from time import sleep

import spacy

from database import models
from translate.google_translate import translate


def add_auto_translation(db):
    not_translated_articles = db.get_not_autotranslated_articles()
    nlp = spacy.load("it_core_news_lg")  # python -m spacy download it_core_news_lg, ru_core_news_lg

    for post in not_translated_articles:
        doc = nlp(post.content)
        for sent in doc.sents:
            text = sent.text
            translation = translate(text)
            print(text, translation)
            payload = {
                "foreign_id": post.foreign_id,
                "sentence_it": text,
                "sentence_ru_auto": translation
            }
            db.add_unique_record(payload, models.Sentences, "sentence_it")
            sleep(randint(1, 10))


def drop_to_excel(db):
    for el in db.get_article_ids():
        df = db.get_not_translated_sentences_df(el)
        filename = os.path.join("for_translation", f"{el}.xlsx")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_excel(filename)

