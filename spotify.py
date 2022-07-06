import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

import warnings
warnings.filterwarnings(action='ignore')

df60s = pd.read_csv("dataset-of-60s.csv")
df70s = pd.read_csv("dataset-of-70s.csv")
df80s = pd.read_csv("dataset-of-80s.csv")
df90s = pd.read_csv("dataset-of-90s.csv")
df00s = pd.read_csv("dataset-of-00s.csv")
df10s = pd.read_csv("dataset-of-10s.csv")

#print(df60s)

#print(df60s.columns)

#target is whether the song is a hit or not 1 = hit song, 0 = not a hit

#this is the full df
#df = pd.concat(map(pd.read_csv, ["dataset-of-60s.csv", "dataset-of-70s.csv", "dataset-of-80s.csv", "dataset-of-90s.csv", "dataset-of-00s.csv", "dataset-of-10s.csv"]), ignore_index = True)
#df.dropna()

##print(df)

#print(df.iloc[-1:])

#print(df.tail())

#checking if df is properly filled ^^

#print(df.info())

dfs = [pd.read_csv(f"dataset-of-{decade}0s.csv") for decade in ['6','7','8','9','0','1']]
print(dfs[1])
for i, decade in enumerate([1960,1970,1980,1990,2000,2010]):
    dfs[i]['decade'] = pd.Series(decade, index = dfs[i].index)

print(dfs[5])



#shuffle our complete df of all decades so that they are not in order

df = pd.concat(dfs, axis = 0).sample(frac = 1.0, random_state = 1).reset_index(drop = True)
print(df)

#check na and drop object because not relevant

print(df.info())


#make a copy for editing and preprocessing
def preprocess(df):
    dfCopy = df.copy()

    #we want to drop categorical values that have nothing to do with our analysis, track name, artist name, and uri (link from spotify api)
    #there are too many elements in these columns we would have to set up too many dummy variables thus making a df with too many cols
    dfCopy = dfCopy.drop(["track", "artist", "uri"], axis = 1)

    #since we predict target (hit or not) we split it

    y = dfCopy["target"]
    x = dfCopy.drop("target", axis = 1)

    #training and testing
    #higher training % = more accuracy, common practice is to use 70/30
    # due to size of our dataset (small) we will use 80/20
    x_train,  x_test, y_train, y_test = train_test_split(x,y, train_size = 0.8, shuffle = True, random_state = 1)

    #scale values to make them closer together

    scale = StandardScaler()
    scale.fit(x_train)
    x_train = pd.DataFrame(scale.transform(x_train), index = x_train.index, columns = x_train.columns)
    x_test = pd.DataFrame(scale.transform(x_test), index = x_test.index, columns = x_test.columns)

    return x_train, x_test, y_train, y_test

x_train, x_test, y_train, y_test = preprocess(df)

print(x_train.var()) #var close to 1
print(x_train.mean()) #mean close to 0

#print(df.var()) variance is too high, must scale in preprocess

#training data
