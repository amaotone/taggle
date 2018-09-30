import json
import re
import urllib
from urllib.parse import urlparse

import firebase_admin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials
from firebase_admin import firestore
from tqdm import tqdm


def fetch_all_competitions():
    page = 1
    competitions = []
    
    while True:
        print(page)
        res = requests.get(f'https://www.kaggle.com/competitions?page={page}')
        res = BeautifulSoup(res.text, 'lxml')
        match = re.findall(r'Kaggle\.State\.push\((\{.*?\})\);', res.text, re.DOTALL)
        body = json.loads(max(match, key=lambda x: len(x)))
        
        if body['fullCompetitionGroups']:
            competitions += max(body['fullCompetitionGroups'], key=lambda x: len(x['competitions']))['competitions']
            competitions += body['pagedCompetitionGroup']['competitions']
        elif body['pagedCompetitionGroup']['competitions']:
            competitions += body['pagedCompetitionGroup']['competitions']
        else:
            break
        page += 1
    
    return competitions


def remove_all_query(url):
    return urllib.parse.urlunparse(urllib.parse.urlparse(url)._replace(query=None))


res = fetch_all_competitions()
res = {c['competitionId']: {
    'name': c['competitionTitle'],
    'url': c['competitionUrl'],
    'image': remove_all_query(c['thumbnailImageUrl']),
    'start': pd.to_datetime(c['enabledDate']),
    'end': pd.to_datetime(c['deadline']),
    'tags': {cat['displayName']: True for cat in c['categories']['categories']}
} for c in res}

cred = credentials.Certificate('./taggle-8cd4d-995fea710484.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'taggle-8cd4d',
})

db = firestore.client()
compe = db.collection('competitions')

for k, v in tqdm(res.items()):
    compe.document(str(k)).set(v)
