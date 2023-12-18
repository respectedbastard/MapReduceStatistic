from fastapi import FastAPI
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

import requests
from textblob import TextBlob
from pydantic import BaseModel
import models
from database import engine


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

main_dict = {}

class Link(BaseModel):
    link: str
@app.get('/clear_db')
def clear_db():
    models.Base.metadata.drop_all(bind=engine)
    return {'База данных': 'успешно очищена'}
#Получение запроса
@app.post("/process")
def count_words(link: Link):
    link = link.link
    response = requests.get(link)
    page = BeautifulSoup(response.content, 'html.parser')
    text = TextBlob(page.get_text())
    text = text.lower()
    words_counter = text.word_counts
    words_counter = dict(sorted(words_counter.items(), key=lambda x: x[1], reverse=True))
        
    return words_counter 

