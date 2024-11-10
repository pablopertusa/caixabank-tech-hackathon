import tensorflow as tf
import pandas as pd
import json
from tensorflow.keras import layers, models, optimizers
from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np


with open('/home/pablo/Desktop/side/caixabank-tech-hackathon/data/raw/columns_datatypes.json', 'r') as f:
    types = json.load(f)

df = pd.read_csv('/home/pablo/Desktop/side/caixabank-tech-hackathon/data/raw/train_downcasted.csv', dtype=types)
print("GPU disponible:", tf.config.list_physical_devices('GPU'))
num_features = len(df.columns)

X = df.drop(columns=['label'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=27)


model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(num_features,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Salida para clasificación binaria (si fuese multiclase softmax)
    ])
optim = optimizers.SGD(learning_rate = 0.001)

model.compile(optimizer = optim, 
                  loss='binary_crossentropy', 
                  metrics=['accuracy', tf.keras.metrics.AUC()])

class_weights = class_weight.compute_class_weight(class_weight='balanced', classes=np.unique(y_train), y=y_train)
class_weights_dict = {'Yes': class_weights['Yes'], 'No': class_weights['No']}

history = model.fit(X_train, y_train, 
                    epochs=20, 
                    batch_size=32, 
                    validation_data=(X_test, y_test),
                    class_weight=class_weights_dict)

y_pred = (model.predict(X_test) > 0.5).astype("int32") # Usando como umbral 0.5

# Métricas de clasificación
print(classification_report(y_test, y_pred))
