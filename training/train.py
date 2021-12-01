import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization, Activation
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from sklearn import metrics
import joblib
from AccuracyCheck import accCheck

data = pd.read_csv("dataset.csv")

x_columns = data.columns.drop('label')
x = data[x_columns]
x = x.values
y = data['label']

le_proto = LabelEncoder()
x[:, 0] = le_proto.fit_transform(x[:, 0])
joblib.dump(le_proto, 'proto.joblib',protocol=1)
le_label = LabelEncoder()
y = le_label.fit_transform(y)
joblib.dump(le_label, 'label.joblib',protocol=1) 
sc = StandardScaler()
x=sc.fit_transform(x)
joblib.dump(sc, 'scaler.joblib',protocol=1)

mdl = Sequential()

mdl.add(Dense(10, activation='relu',input_shape = (8,)))
mdl.add(Dense(10, activation='relu'))
mdl.add(Dense(10, activation='relu'))
mdl.add(Dense(7, activation='softmax'))
mdl.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
mdl.summary()

save_checkpoint = ModelCheckpoint( filepath = 'trained_model.h5', monitor = 'val_accuracy', save_best_only = True, save_weights_only = False, mode = 'auto')

learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience=5, verbose=1, factor=0.5, min_lr=0.0001)

history = mdl.fit(x, y, batch_size=64, validation_split=0.3,callbacks=[save_checkpoint], epochs=50 ,shuffle=False)


mdl = load_model('trained_model.h5')
datatest = pd.read_csv("datatest.csv")
x_columns = datatest.columns.drop('label')
x = datatest[x_columns].values
y = datatest['label']

x[:, 0] = le_proto.transform(x[:, 0])
y = le_label.transform(y)
x=sc.transform(x)

stats = {}
labels = ['normal','tcpsynflood','icmpflood','udpflood','ipsweep','portscan','pingofdeath']

y_pred = np.argmax(mdl.predict(x), axis = 1)
y_pred = le_label.inverse_transform(y_pred)
y_test = le_label.inverse_transform(y)

for i in labels:
    stats[i]={}
    for j in labels:
        stats[i][j] = 0

for i in range(len(y)):
    stats[y_test[i]][y_pred[i]] += 1

accCheck(stats)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
