import pandas as pd
from sqlalchemy import create_engine
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from catboost import CatBoostClassifier, Pool, metrics, cv

import os
import numpy as np

con = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
engine = create_engine(con)

# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def get_embddings(texts):
    # Tokenize sentences
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    return sentence_embeddings

def make_embddings():
    text_embeds_path = 'text_embeds.csv'
    if not os.path.exists(text_embeds_path):
        texts = pd.read_sql("select distinct * from public.post_text_df", engine)
        matrix = pd.DataFrame()

        for chunk in tqdm(np.array_split(texts, 100)):
            embeds = get_embddings(chunk['text'].values.tolist())
            res = pd.concat([chunk['post_id'].reset_index(drop=True).rename('post_id'), pd.DataFrame(embeds)], axis=1, ignore_index=True)
            res = res.rename(columns={0: 'post_id'})
            matrix = pd.concat([matrix, res], axis=0)

        matrix.to_csv(text_embeds_path)
    else:
        matrix = pd.read_csv(text_embeds_path)
        
    return matrix

def build_dataset():
    matrx = make_embddings()
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
    df = pd.read_sql(query, engine).iloc[:, [0,1,2,4,7,9,10,11,12,13,14,15]]
    dfm = df.merge(matrix, how='left', on='post_id').drop(columns=['Unnamed: 0'])
    dfm = dfm.rename(columns = lambda x: f'emb_{x}' if x.isdigit() else x)
    return dfm
    
def fit_model():
    dfm = build_dataset()
    train, test = dfm[dfm['timestamp'] <= '2021-12-12'], dfm[dfm['timestamp'] > '2021-12-12']

    X_train, y_train = train.drop(columns=['target', 'user_id', 'post_id', 'timestamp']), train['target']
    X_test, y_test = test.drop(columns=['target', 'user_id', 'post_id', 'timestamp']), test['target']
    
    catboost_model = CatBoostClassifier(learning_rate=0.02)

    cat_features = ['topic', 'gender', 'age', 'country', 'city', 'exp_group', 'os', 'source']
    catboost_model.fit(X_train, y_train, cat_features=cat_features)

    catboost_model.save_model('catboost_model',
                               format="cbm")

    from_file = CatBoostClassifier()  # здесь не указываем параметры, которые были при обучении, в дампе модели все есть

    from_file.load_model("catboost_model")

    from_file.predict(X_train)

def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":  # проверяем где выполняется код в лмс, или локально. Немного магии
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH

def load_models():
    model_path = get_model_path("/my/super/path")
    model = pickle.load(model_path) # пример как можно загружать модели