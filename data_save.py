import os
from sqlalchemy import create_engine
import pymysql

def save2disk(name,result):
    file=os.getcwd()+"/"+name+".txt"
    output=open(file,'a',encoding='utf-8')
    output.write(result)
    output.close()


# create_engine('dialect+driver://username:password@host:port/database')
def save2sql(name,df):
    connection = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format('root', '123456', '127.0.0.1', '3306',
                                                                                  'house', 'utf8mb4'))
    # 虽然原数据不含id，但是这里生成的id没有列名，所以不能在这里生成，index=false
    df.to_sql(name, connection, if_exists='replace', index=False)