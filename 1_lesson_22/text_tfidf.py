import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import numpy as np
import pickle

con = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
engine = create_engine(con)

def get_embddings(texts):
    vectorizer = TfidfVectorizer(max_features=300)
    # Tokenize sentences
    embeds = vectorizer.fit_transform(texts).todense()
    embeds = pd.DataFrame(embeds).rename(columns=lambda x: f'emb_{x}')

    return vectorizer, embeds

def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":  # проверяем где выполняется код в лмс, или локально. Немного магии
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH

def load_models():
    model_path = get_model_path("/my/super/path")
    model = pickle.load(model_path) # пример как можно загружать модели

query = """
with fd as (
    select
        *
    from public.feed_data
    where 1=1 
    and action = 'view' -- т.к. есть столбец target, то уже на нём можно обучить модель классификации
    and user_id in (select user_id from (select distinct user_id from public.feed_data) tt where random() < 0.02)
    -- and user_id = '113330'
)
select *
from fd
left join (select * from public.post_text_df) ptd on fd.post_id = ptd.post_id
left join public.user_data ud on ud.user_id = fd.user_id
limit 100000
"""
# df = pd.read_sql(query, engine)
df = pd.read_sql(query, engine).iloc[:, [0,1,2,4,6,7,9,10,11,12,13,14,15]]
vectorizer, embeds_df = get_embddings(df['text'])
dfm = pd.concat([df.drop(columns=['text']), embeds_df], axis=1)

train, test = dfm[dfm['timestamp'] <= '2021-12-12'], dfm[dfm['timestamp'] > '2021-12-12']

X_train, y_train = train.drop(columns=['target', 'user_id', 'post_id', 'timestamp']), train['target']
X_test, y_test = test.drop(columns=['target', 'user_id', 'post_id', 'timestamp']), test['target']

from catboost import CatBoostClassifier, Pool, metrics, cv
catboost_model = CatBoostClassifier(learning_rate=0.02)

cat_features = ['topic', 'gender', 'age', 'country', 'city', 'exp_group', 'os', 'source']
catboost_model.fit(X_train, y_train, cat_features=cat_features)

catboost_model.save_model('catboost_model',
                           format="cbm")

from_file = CatBoostClassifier()  # здесь не указываем параметры, которые были при обучении, в дампе модели все есть

from_file.load_model("catboost_model")

from_file.predict(X_train)