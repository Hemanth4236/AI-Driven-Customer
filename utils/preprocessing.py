import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df):

    df = df.copy()

    le_gender = LabelEncoder()

    df['Gender'] = le_gender.fit_transform(df['Gender'])

    return df