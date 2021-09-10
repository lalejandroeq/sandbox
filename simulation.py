import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


def dates_generator(input_date, rounds):
    max_train_date = datetime.strptime(input_date, '%Y-%m-%d')
    prediction_date = max_train_date - timedelta(days=1)
    yield prediction_date.strftime('%Y-%m-%d'), max_train_date.strftime('%Y-%m-%d')
    for i in range(rounds):
        max_train_date = max_train_date + timedelta(days=1)
        prediction_date = max_train_date - timedelta(days=1)
        yield prediction_date.strftime('%Y-%m-%d'), max_train_date.strftime('%Y-%m-%d')


def build_ds_splits(train_df, prediction_df):
    # Process training
    X_train = train_df.iloc[:, 1:27]
    Y_train = train_df.iloc[:, 27]

    # Process prediction
    X_test = prediction_df.iloc[:, 1:27]
    Y_test = prediction_df.iloc[:, 27]

    return X_train, Y_train, X_test, Y_test


def classify(x_train, y_train, x_test):
    model = XGBClassifier(verbosity=0)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    return y_pred


if __name__ == '__main__':
    date_time_str = '2021-03-01'
    df = pd.read_csv("test.csv")
    df["P1_Open"] = (df["Open"] - df.shift(1)["Open"])/df.shift(1)["Open"]
    df["P2_Open"] = (df["Open"] - df.shift(2)["Open"])/df.shift(2)["Open"]
    df["P3_Open"] = (df["Open"] - df.shift(3)["Open"])/df.shift(3)["Open"]
    df["P4_Open"] = (df["Open"] - df.shift(4)["Open"])/df.shift(4)["Open"]
    df["P5_Open"] = (df["Open"] - df.shift(5)["Open"])/df.shift(5)["Open"]
    df["P6_Open"] = (df["Open"] - df.shift(6)["Open"]) / df.shift(6)["Open"]
    df["P7_Open"] = (df["Open"] - df.shift(7)["Open"]) / df.shift(7)["Open"]
    df["P8_Open"] = (df["Open"] - df.shift(8)["Open"]) / df.shift(8)["Open"]
    df["P9_Open"] = (df["Open"] - df.shift(9)["Open"]) / df.shift(9)["Open"]
    df["P10_Open"] = (df["Open"] - df.shift(10)["Open"]) / df.shift(10)["Open"]
    df["P1_Volume"] = (df["Volume"] - df.shift(1)["Volume"])/df.shift(1)["Volume"]
    df["P2_Volume"] = (df["Volume"] - df.shift(2)["Volume"])/df.shift(2)["Volume"]
    df["P3_Volume"] = (df["Volume"] - df.shift(3)["Volume"])/df.shift(3)["Volume"]
    df["P4_Volume"] = (df["Volume"] - df.shift(4)["Volume"])/df.shift(4)["Volume"]
    df["P5_Volume"] = (df["Volume"] - df.shift(5)["Volume"])/df.shift(5)["Volume"]
    df["P6_Volume"] = (df["Volume"] - df.shift(6)["Volume"]) / df.shift(6)["Volume"]
    df["P7_Volume"] = (df["Volume"] - df.shift(7)["Volume"]) / df.shift(7)["Volume"]
    df["P8_Volume"] = (df["Volume"] - df.shift(8)["Volume"]) / df.shift(8)["Volume"]
    df["P9_Volume"] = (df["Volume"] - df.shift(9)["Volume"]) / df.shift(9)["Volume"]
    df["P10_Volume"] = (df["Volume"] - df.shift(10)["Volume"]) / df.shift(10)["Volume"]
    # df["Delta_Price"] = (df["Open"] - df["Close"]) / df["Open"]
    df["Class"] = np.where((df.shift(-1)["Open"] - df["Open"])/df["Open"] > 0.01, 1, 0)
    df = df[df["P10_Open"].notnull()]
    df = df[df["Class"].notnull()]

    profit = 0
    for t_date, p_date in dates_generator(date_time_str, 30):

        t_df = df[(df['Date'] <= t_date)].copy()
        p_df = df[(df['Date'] == p_date)].copy()
        try:
            buy_price = df[(df['Date'] == t_date)]['Open'].values[0]
            sell_price = p_df['Open'].values[0]
        except IndexError:
            continue
        # print(buy_price, sell_price)

        x_train, y_train, x_test, y_test = build_ds_splits(t_df, p_df)
        y_pred = classify(x_train, y_train, x_test)
        if y_pred[0] == 1:
            profit += buy_price - sell_price

    print(profit)


