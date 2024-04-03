from fastapi import FastAPI
from bs4 import BeautifulSoup

import requests
from textblob import TextBlob
from schemas import Link



app = FastAPI()



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

