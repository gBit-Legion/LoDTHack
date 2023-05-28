import os
import re
import pickle
import numpy as np
import pandas as pd
import collections
from pathlib import Path
from random import randrange
from datetime import datetime

import psycopg2
from loguru import logger
from dotenv import load_dotenv
from geopy.geocoders import Nominatim, Yandex

from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

import gensim
from clasterisation.miniBatch import MiniBatch
from classification.ml import MiniBatchClf

# Загрузка предобученных моделей обработки текста (кластеризация).
cls_path = Path().cwd().joinpath('clasterisation')
minibatchkmeans = 0
word2vec = gensim.models.Word2Vec.load(str(cls_path.joinpath('word2vec.model')))
with open(str(cls_path.joinpath('kmeans-clust.pkl')), 'rb') as f:
    minibatchkmeans = pickle.load(f)
logger.success('Cluster Model loading succesful!')

# Загрузка предобученных моделей обработки текста (классификация).
clf_path = Path().cwd().joinpath('classification')
sk_model = 0
w2v_model = gensim.models.Word2Vec.load(str(clf_path.joinpath('word2vec.model')))
with open(str(clf_path.joinpath('rf_model.pkl')), 'rb') as fid:
    sk_model= pickle.load(fid)
logger.success('Classifyer Model loading succesful!')

# Внесение конфига для подключения к БД (не важно где она)
load_dotenv('../DB.ENV', override=True)
SOURCE = os.environ.get('SOURCE')
GEOCODER = os.environ.get('GEOCODER')

# Геокодер для отобраджения на карте полученных отзывов
if GEOCODER == 'YANDEX':
    try:
        GEOCODER = Yandex(api_key=os.environ.get('YANDEX_API'), user_agent="POSTAMAT PROJECT")
        logger.success('Using API-Yandex GEOCODER')
    except Exception as e:
        logger.error(e)
elif GEOCODER == 'DEFAULT':
    try:
        GEOCODER = Nominatim(user_agent="POSTAMAT PROJECT")
        logger.success('Using default OpenStreetMap GEOCODER ')
    except Exception as e:
        logger.error(e)

# Инициализация переменных
conn = 0
cur = 0
old_stats = 0
DEBUG = True
# Костыльные словари для пользователей \ операторов
CLASSIFICATOR_CLASSES = {
    '0' : 'good',
    '1' : 'article',
    '2' : 'delivery',
    '3' : 'post',
    '4' : 'times'
}
CLASSIFICATOR_RUS_CLASSES = {
    '0' : 'Все хорошо',
    '1' : 'Проблема с товаром',
    '2' : 'Проблема с доставкой',
    '3' : 'Проблема с постаматом (ПВЗ)',
    '4' : 'Проблема со сроками'
}
MONTH_NAMES = {
    '1' : 'january',
    '2' : 'february',
    '3' : 'march',
    '4' : 'april',
    '5' : 'may',
    '6' : 'june',
    '7' : 'july',
    '8' : 'august',
    '9' : 'september',
    '10' : 'october',
    '11' : 'november',
    '12' : 'december'
}

# Попытка подключения к БД в Докере, На удаленной машине, На локальном компе
try:  
    IP = 0
    if SOURCE == 'Host':
        logger.debug(SOURCE)
    # Получение конфига 
        IP=os.environ.get("HOST_IP")
    elif SOURCE == 'Docker':
        logger.debug(SOURCE)
        IP=os.environ.get("DOCKER_CONTAINER_DB_NAME")
    PORT=os.environ.get("PORT")
    DBNAME=os.environ.get("POSTGRES_DATABASE")
    USER=os.environ.get("POSTGRES_USER")
    PASSWORD=os.environ.get("POSTGRES_PASSWORD")

    logger.debug(f'{SOURCE} connection started, {IP}, {PORT}, {DBNAME}, {USER}, {PASSWORD},  - env variables!')
    
    conn = psycopg2.connect(
        dbname=DBNAME, 
        host=IP, 
        user=USER, 
        password=PASSWORD, 
        port=PORT)

    cur = conn.cursor()

    logger.success(f'{SOURCE} connected!')

except Exception as e:
    logger.error(f'{SOURCE} connect failed \n {e}!')

# Функции-обертки
# Реализация координат для адреса (в приоритете - использовать яндекс карты, т.к. иногда дефолтный геокодер путается)
def String2Coords(adress):
    adress = re.sub(' к. [0-9999],', '', adress)
    adress = adress.replace('б-р. ', 'бульвар ')
    adress = adress.replace('ш. ', 'шоссе ')
    try:
        location = GEOCODER.geocode(adress, language='ru')
        data = location.latitude, location.longitude
        return location.latitude, location.longitude
    except Exception as e:
        logger.error(f'Wrong adress! \n {adress}')
        logger.error(e)
    
# Функция - предсказание класса (машинное обучение)
def String2Classs(usertext, word2vec, minibatchclf):
    return MiniBatchClf(usertext, word2vec, minibatchclf)

# Функция - анализ кластера (машинное обучение)
def String2Cluster(usertext, word2vec, minibatch):
    return MiniBatch(usertext, word2vec, minibatch)

# Заглушка чистой воды, если пользователь обращается не по приложению обратной связи
# ЗАГЛУШКА под номера заказов! ---------------
def SomeArticleFromYourSources():
    return randrange(0, 9999999, 1)
# Конец заглушки -----------------------------

# Функция-поддержка для вывода обозначений классов 
def Number2Class(code):
    return CLASSIFICATOR_CLASSES[f'{str(code)}']

# Функция-поддержка для вывода обозначений классов 
def Number2RusClass(code):
    return CLASSIFICATOR_RUS_CLASSES[f'{str(code)}']

# Функция-поддержка для вывода обозначений классов 
def Number2Month(code):
    return MONTH_NAMES[f'{str(code)}']

# Статистика адресов во входном запросе
def getAdressStats(result):
    stats = []
    adresses = collections.Counter([x['adress'] for x in result])
    unique_adresses = list(set(adresses.elements()))
    for adress in unique_adresses:
        substats = {
            'adress': adress,
            'stars': np.mean([float(subresult['mark']) for subresult in result if subresult['adress'] == adress]),
            'textnumbers': len([subresult['usertext'] for subresult in result if subresult['adress'] == adress]),
            'problem': Number2RusClass(collections.Counter([int(subresult['classnumber']) for subresult in result if subresult['adress'] == adress]).most_common(1)[0][0])
        }
        stats.append(substats)
    if DEBUG:
        logger.debug(stats)
    return stats

# Статистика для макретплейсов
def getMarketStats(result):
    stats = []
    markets = collections.Counter([x['seller'] for x in result])
    unique_markets = list(set(markets.elements()))
    for adress in unique_markets:
        substats = {
            'market': adress,
        }
        substats.update(collections.Counter([Number2Class(x['classnumber']) for x in result]))
        stats.append(substats)

    # ЗАГЛУШКА ПОД ДОПОЛНИТЕЛЬНЫЕ МАРКЕТПЛЕЙСЫ -------------
    # В ПРОДЕ - УДАЛЯЙ
    datapatch = collections.Counter([Number2Class(x['classnumber']) for x in result[:len(result) // 2]])
    substats = {
        'market': 'Главпиво'
    }
    substats.update(datapatch)
    stats.append(substats)
    # КОНЕЦ ЗАГЛУШКИ ---------------------------------------
    if DEBUG:
        logger.debug(stats)
    return stats

# Статистика для бейджей вверху страницы для общего понимания сколько запросов в базе
def getTotalStats(result):
    posts = collections.Counter([x['adress'] for x in result])
    markets = collections.Counter([x['seller'] for x in result])
    unique_posts = len(list(set(posts.elements())))
    unique_markets = len(list(set(markets.elements())))
    total_reviews = len(result)
    stats = {
        'postamats': unique_posts,
        'partners': unique_markets,
        'reviews': total_reviews
    }
    if DEBUG:
        logger.debug(stats)
    return stats

# Статистика по классам
def getClassesStats(result):
    stats = {}
    stats.update(collections.Counter([Number2Class(x['classnumber']) for x in result]))
    if DEBUG:
        logger.debug(stats)
    return stats

# Статистика по месяцам
def getTimeStats(result):
    stats = []
    data = collections.Counter([int(datetime.fromisoformat(x['reviewdate']).timestamp()) for x in result])
    keys = list(data.keys())
    values = list(data.values())
    
    for index in range(len(keys)):
        substats = []
        substats.append(keys[index])
        substats.append(values[index])

        stats.append(substats)
    if DEBUG:
        logger.debug(stats)
    return stats

# Бэк на FastAPI
app = FastAPI()

# Безопасность на Ваш выбор. Пока что - брешь в обороне
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Классы для работы с POST-запросами
# Получение отзыва с универсальныго источника (generic для всех остальных)
class ReviewFromAnySource(BaseModel):
    usertext: str
    mark: float
    reviewdate: str
    adress: Union[str, None] = None
    clusternumber: Union[int, None] = None
    classnumber: Union[int, None] = None
    article: Union[str, None] = None
    seller: Union[str, None] = None
    latitude: Union[float, None] = None
    longitude: Union[float, None] = None

# Фича с разметкой данных для улучшения работы Bert
class ReviewFromDatasetFormer(ReviewFromAnySource):
    classnumber: int
    id_: int

class AdminFilter(BaseModel):
    stars: Union[str, list, None] = None 

# Сбор инфы по карте - адреса, отзывы, их количество и т.д
@app.get("/getAdminPageData/")
def adminPage():

    # if item.stars == None:
        # cur.execute(f"SELECT * FROM xdataset")
    # elif type(item.stars) == type([1,2,3]):
    #     cur.execute(f"SELECT * FROM xdataset WHERE mark IN (%s)", item.stars)
    # else:
    #     cur.execute(f"SELECT * FROM xdataset WHERE mark IN (%s)", item.stars)
    logger.debug('Here')
    cur.execute(f"SELECT * FROM reviews")
    data = cur.fetchall()
    result = []
    for index, subdata in enumerate(data):
        usertext = subdata[0]
        mark = subdata[1]
        adress = subdata[2]
        reviewdate = subdata[3]
        clusternumber = subdata[4]
        article = subdata[5]
        seller = subdata[6]
        latitude = subdata[8]
        longitude = subdata[7]
        classnumber = subdata[9]

        result.append({
                "id": index,
                "usertext": usertext,
                "mark": mark,
                "adress": adress,
                "reviewdate": str(reviewdate),
                "clusternumber": clusternumber,
                "article": article,
                "seller": seller,
                "latitude": latitude,
                "longitude": longitude,
                "classnumber": classnumber,
                "namedclassnumber": Number2RusClass(classnumber)
            })
    
    adressStats = getAdressStats(result)
    marketStats = getMarketStats(result)
    totalStats = getTotalStats(result)
    classStats = getClassesStats(result)
    timeStats = getTimeStats(result)

    total_data = {
        "data": result,
        'adressStats': adressStats,
        'marketStats': marketStats,
        'totalStats': totalStats,
        'classStats': classStats,
        'timeStats': timeStats
    }

    return JSONResponse(status_code=200, content=total_data)

# API для добавления универсального отзыва с обработкой ГЕОЛОКАЦИИ + КЛАСТЕРИЗАЦИИ + КЛАССИФИКАЦИИ + ВАШ ИСТОЧНИК НОМЕРА ЗАКАЗА
@app.post("/addReview/")
def intellegenceReviewProceduring(item: ReviewFromAnySource):
    # Логика обработки адресов, кластеров и классов + на ваш выбор что хотите
    
    # Координаты, проверка на адекватность запроса
    if item.adress:
        try: 
            latitude, longitude = String2Coords(item.adress)
        except:
            return Response(status_code=422)
    else:
        return Response(status_code=422)
    
    # Если с формы не поступает класс, то размечаем его
    if item.classnumber != -999:
        classnumber = item.classnumber
    else:
        # Если запрос не битый - то класс и кластер указываем
        if item.usertext:
            classnumber = int(String2Classs(item.usertext, w2v_model, sk_model)[0])
        else:
            return Response(status_code=422)
    
    # Если с формы не прилетает номер кластера, то предсказываем его
    if item.clusternumber != -999:
        clusternumber = item.clusternumber
    else:
        # Если запрос не битый - то класс и кластер указываем
        if item.usertext:
            clusternumber = int(String2Cluster(item.usertext, word2vec, minibatchkmeans)[0])
        else:
            return Response(status_code=422)

    
    # ЗАГЛУШКА!!! --------------------------------
    article = SomeArticleFromYourSources()
    # КОНЕЦ ЗАГЛУШКИ -----------------------------

    # Проверка на адекватност передаваемой даты
    try:
        reviewdate = datetime.fromisoformat(item.reviewdate.replace('T', ' ').split('.')[0])
    except Exception as e:
        logger.debug(item.reviewdate)
        logger.error(f'Datetime error! \n {e}')
        return Response(status_code=422)

    # Контроль
    if DEBUG:
        logger.success('User text -- ' + item.usertext)
        logger.success('Mark -- ' + str(item.mark))
        logger.success('Adress -- ' + str(item.adress))
        logger.success('Review date -- ' + str(reviewdate))
        logger.success('Cluster number (Optional) -- ' + str(clusternumber))
        logger.success('Class number (Optional) -- ' + str(classnumber))
        logger.success('Article (Optianal) -- ' + str(article))
        logger.success('Seller (Optional) -- ' + str(item.seller))
        logger.success('Longitude (Optional) -- ' + str(longitude))
        logger.success('Latitude (Optional) -- ' + str(latitude))

    cur.execute("""
    INSERT INTO reviews 
        (usertext, mark, adress, reviewdate, clusternumber, article, seller, longitude, latitude, classnumber) 
    VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
    (item.usertext, item.mark, item.adress, reviewdate, clusternumber, article, item.seller, longitude, latitude, classnumber))    
    conn.commit()

    return Response(status_code=201)

# API для датасета (получение случайной строчки из БД  + удаление из сырых данных)
@app.get("/getFormDatasetElement/")
def getDatasetFormerElement():
    # Подсчитываем сколько строк в таблице
    cur.execute("""SELECT COUNT(*) FROM rawdataset;""")
    result = cur.fetchall()
    for index, data in enumerate(result):
        result = data[0]

    # Выбираем случайную строку
    try:
        randomRow = randrange(1, result, 1)
        cur.execute(f"""SELECT * FROM rawdataset WHERE id = {randomRow};""")
        row = cur.fetchall()
        for index, subdata in enumerate(row):
            usertext = subdata[0]
            mark = subdata[1]
            adress = subdata[2]
            reviewdate = subdata[3]
            clusternumber = subdata[4]
            article = subdata[5]
            seller = subdata[6]
            latitude = subdata[7]
            longitude = subdata[8]
            id_ = subdata[9]

    except UnboundLocalError as e:
        logger.error(e)
        randomRow = randrange(1, result, 1)
        cur.execute(f"""SELECT * FROM rawdataset WHERE id = {randomRow};""")
        row = cur.fetchall()
        for index, subdata in enumerate(row):
            usertext = subdata[0]
            mark = subdata[1]
            adress = subdata[2]
            reviewdate = subdata[3]
            clusternumber = subdata[4]
            article = subdata[5]
            seller = subdata[6]
            latitude = subdata[7]
            longitude = subdata[8]
            id_ = subdata[9]

    try:
        # Удаляем строчку с такими данными
        cur.execute(f"""DELETE FROM rawdataset WHERE id = {id_};""")
        conn.commit()
    except Exception as e:
        logger.error(e)
        conn.rollback()

    # Для статистики и отслеживания сколько экземпляров для классов есть.
    # Поможет когда будете создавать свой датасет на своих отзывах
    try:
        results = []
        for classIndex in range(0,5,1):
            cur.execute(f"""SELECT COUNT(*) FROM xdataset WHERE classnumber = {classIndex};""")
            result = cur.fetchall()
            subresult = result[0][0]
            results.append(subresult)
        old_stats = results
    except psycopg2.ProgrammingError as e:
        logger.error(e)
        results = old_stats
    if DEBUG:
        logger.debug("Dataset balance -- " + str(results))
    
    jsoned = {
        "usertext": usertext, 
        "mark": mark,
        "adress" :adress, 
        "reviewdate": str(reviewdate),
        "clusternumber": clusternumber, 
        "article": article, 
        "seller": seller, 
        "latitude": latitude, 
        "longitude": longitude,
        "id_": id_,
        "stats": results
    }

    return JSONResponse(content=jsoned, status_code=200)

# API для датасета (добавление в таблицу с выборкой)
@app.post("/addFormDatasetElement/")
def addDatasetFormerElement(item: ReviewFromDatasetFormer):
    
    # Если данные верны - оправляем на БД
    if item.usertext:
        # Контроль
        if DEBUG:
            logger.success('User text -- ' + item.usertext)
            logger.success('ID -- ' + str(item.id_))
            logger.success('Mark -- ' + str(item.mark))
            logger.success('Adress -- ' + str(item.adress))
            logger.success('Review date -- ' + str(item.reviewdate))
            logger.success('Cluster number (Optional) -- ' + str(item.clusternumber))
            logger.success('Article (Optianal) -- ' + str(item.article))
            logger.success('Seller (Optional) -- ' + str(item.seller))
            logger.success('Longitude (Optional) -- ' + str(item.longitude))
            logger.success('Latitude (Optional) -- ' + str(item.latitude))    
            logger.success('Marked class -- ' + str(item.classnumber))    

    try:
        cur.execute("""
            INSERT INTO xdataset 
                (usertext, mark, adress, reviewdate, clusternumber, article, seller, longitude, latitude, classnumber) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (item.usertext, str(item.mark), item.adress, item.reviewdate, item.clusternumber, item.article, item.seller, item.longitude, item.latitude, item.classnumber))    
    except Exception as e:
        logger.error(e)
        conn.rollback()
        return Response(status_code=304)
    
    return Response(status_code=201)

# Отчет по постаматам и проблемам
@app.get('/getAdminPageAdressStatsFile/')
def adminPageAdressStatsFile():
    cur.execute(f"SELECT * FROM xdataset")
    data = cur.fetchall()
    result = []
    for index, subdata in enumerate(data):
        usertext = subdata[0]
        mark = subdata[1]
        adress = subdata[2]
        reviewdate = subdata[3]
        clusternumber = subdata[4]
        article = subdata[5]
        seller = subdata[6]
        latitude = subdata[7]
        longitude = subdata[8]
        classnumber = subdata[9]

        result.append({
                "id": index,
                "usertext": usertext,
                "mark": mark,
                "adress": adress,
                "reviewdate": str(reviewdate),
                "clusternumber": clusternumber,
                "article": article,
                "seller": seller,
                "latitude": latitude,
                "longitude": longitude,
                "classnumber": classnumber
            })

    adressStats = getAdressStats(result)
    df = pd.DataFrame(columns=['adress', 'stars', 'textnumbers', 'problem'])
    for index_, dictionary in enumerate(adressStats):
        extended = pd.DataFrame(dictionary, index=[index_])
        df = pd.concat([df,extended], ignore_index=True)

    path = "report.csv"
    df.to_csv(path)
    return FileResponse(path=path, status_code=200, media_type='multipart/form-data')
    
# Отчет по отзывам и проблемам
@app.get('/getAdminPageClassesStatsFile/')
def adminPageClassesStatsFile():
    cur.execute(f"SELECT * FROM xdataset")
    data = cur.fetchall()
    result = []
    for index, subdata in enumerate(data):
        usertext = subdata[0]
        mark = subdata[1]
        adress = subdata[2]
        reviewdate = subdata[3]
        clusternumber = subdata[4]
        article = subdata[5]
        seller = subdata[6]
        classnumber = subdata[9]

        result.append({
                "usertext": usertext,
                "mark": mark,
                "adress": adress,
                "reviewdate": str(reviewdate),
                "clusternumber": clusternumber,
                "article": article,
                "seller": seller,
                "classnumber": Number2RusClass(classnumber)
            })
        
    df = pd.DataFrame(columns=["usertext", "mark", "adress", "reviewdate", "clusternumber", "article", "seller", "classnumber"])
    for index_, dictionary in enumerate(result):
        extended = pd.DataFrame(dictionary, index=[index_])
        df = pd.concat([df,extended], ignore_index=True)

    path = "report.csv"
    df.to_csv(path)
    return FileResponse(path=path, status_code=200)

