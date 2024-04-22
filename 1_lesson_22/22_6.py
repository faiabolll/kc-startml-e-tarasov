import pandas as pd
from sqlalchemy import create_engine

def upload_features(feats):
    con = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    engine = create_engine(con)
    feats.iloc[:6000000, :].to_sql('e_tarasov_22_6', con=engine)
    
    

def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    con = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    engine = create_engine(con)
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)

def load_features(query):
    batch_load_sql(query)