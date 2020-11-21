import pandas as pd
from sqlalchemy import create_engine


def create_engine_for_final_db():
    engine = create_engine('postgresql://django@68.226.133.212:5440/final_lstm_db')
    return engine


def get_dataframe(stock):
    data = pd.read_sql(stock, create_engine_for_final_db())
    return data


df = get_dataframe('GE')
print(df.head())
df = df.to_csv("data_csv_GE.csv")
