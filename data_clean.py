import pandas as pd


def clean(dictionary):
    df = pd.DataFrame(data=dictionary)
    # 删除'name'相同的重复数据,不取代原来的值
    data2 = df.drop_duplicates(subset='name',inplace=False)
    #把price用0填充
    data2.loc[:,"price"]=data2["price"].fillna("0")

    data2['price']=pd.to_numeric(data2['price'])
    data2.loc[:,'id']=[str(x) for x in range(len(data2))]
    data2['id']=pd.to_numeric(data2['id'])
    return data2
    pass
