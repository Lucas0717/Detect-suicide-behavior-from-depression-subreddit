import pandas as pd
from app2 import *
from csv import reader
import pickle
from sklearn.feature_extraction.text import CountVectorizer

def predict_result():
    # open file in read mode
    a = []
    with open('parameters.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            a.append(row)
    dep_columns,sui_columns = a[0],a[1]

    new_depression_df = pd.read_csv('./past_7days/depression.csv')
    new_depression_df = new_depression_df.dropna(axis=0)
    corpus = new_depression_df['tibo'].apply(lambda x: ' '.join(x)).str.replace(r"\s+(.)\1+\b", "").str.strip().tolist()

    mnb1 = pickle.load(open('depression_model.sav','rb'))
    mnb2 = pickle.load(open('suicide_model.sav','rb'))
    # predict by depression model
    vectorizer6 = CountVectorizer(vocabulary=dep_columns)
    V6 = vectorizer6.fit_transform(corpus)
    df6 = pd.DataFrame(V6.toarray())
    df6.columns = vectorizer6.get_feature_names()
    df6 = df6.drop(['class'], axis=1)
    predict_dep = mnb1.predict(df6)
    # depression by suicide model
    vectorizer7 = CountVectorizer(vocabulary=sui_columns)
    V7 = vectorizer7.fit_transform(corpus)
    df7 = pd.DataFrame(V7.toarray())
    df7.columns = vectorizer7.get_feature_names()
    df7 = df7.drop(['class'], axis=1)
    predict_sui = mnb2.predict(df7)
    pro_sui = mnb2.predict_proba(df7)
    # get top10 suicide post and information
    suicide_pro_dict = {}
    for i in range(len(predict_dep)):
        if predict_dep[i] == 1 and predict_sui[i] == 1:
            suicide_pro_dict[i] = pro_sui[i][1]
    sorted_suicide = dict(sorted(suicide_pro_dict.items(), key=lambda item: -item[1]))
    k = list(sorted_suicide.keys())[:15]
    v = list(sorted_suicide.values())[:15]
    order_frame = new_depression_df.iloc[k]
    order_frame['prob'] = v
    return order_frame