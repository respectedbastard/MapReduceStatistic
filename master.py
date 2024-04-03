from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
from database import engine

from time import time

import asyncio
import aiohttp

from settings import settings

cash_dict = {}

app = FastAPI()

class Links(BaseModel):
    get_links: List[str]




@app.post('/get_result/')
async def main(links: Links): 
    start_time = time()
    links_for_slave = [list() for _ in range(settings.slave_quantity)]
    counter = 0
    for link in links.get_links:
        if counter > settings.slave_quantity - 1:
            counter = 0
        links_for_slave[counter].append(link)
        counter += 1
    for i in range(settings.slave_quantity):
        await process_links(links_for_slave[i], f'http://localhost:900{i+1}/process')
    
    clear_cash()
    end_time = time()
    return {'База данных': f'успешно обновлена за {end_time-start_time}'} 

async def process_links(links, url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for request in links:
            request = {'link': request}
            tasks.append(asyncio.ensure_future(fetch(session, url, request)))
        await asyncio.gather(*tasks)

async def fetch(session, url, request):
    async with session.post(url, json=request) as response:
        response_dict = await response.json()
        cash(response_dict)



def cash(response_dict):
    counter = 0
    for word, value in response_dict.items():
        if word in cash_dict:
            cash_dict[word] += value
        elif word not in cash_dict and counter < settings.cash_capacity:
            cash_dict[word] = value
            counter += 1
        else:
            to_db = list(cash_dict.items())[int(settings.cash_capacity*0.2):] 
            for elem in to_db:
                word_to_db, value_to_db = elem
                push_data(word_to_db, value_to_db) 
            
 

def clear_cash():
    with Session(autoflush=True, bind=engine) as db:
        for word, value in cash_dict.items():
            is_word = db.query(models.WordCount).filter_by(word=word).first()
            if is_word:
                is_word.count += value
                db.commit()
            else:
                elem = models.WordCount(word=word, count=value)
                db.add(elem)
                db.commit()
    cash_dict.clear()
            


def push_data(word, value):
    with Session(autoflush=True, bind=engine) as db:
        is_word = db.query(models.WordCount).filter_by(word=word).first()
        if is_word:
            is_word.count += value
            db.commit()
        else:
            elem = models.WordCount(word=word, count=value)
            db.add(elem)
            db.commit()


@app.get('/get_first')
def get_first(value: int):
    with Session(autoflush=True, bind=engine) as db:
        words = db.query(models.WordCount).order_by(models.WordCount.count.desc()).limit(value).all()
    return words


@app.get('/clear_db')
def delete():
    with Session(autoflush=True, bind=engine) as db:
        db.query(models.WordCount).delete()
        db.commit()
        return {'Таблица': 'успешно очищена'}