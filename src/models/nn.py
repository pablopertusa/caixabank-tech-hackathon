import tensorflow as tf
import pandas as pd
import json
from tensorflow.keras import layers, models
from sklearn.utils import class_weight

with open('/home/pablo/Desktop/side/caixabank-tech-hackathon/data/raw/columns_datatypes.json', 'r') as f:
    types = json.load(f)

#df = pd.read_csv('/home/pablo/Desktop/side/caixabank-tech-hackathon/data/raw/train_downcasted.csv', dtype=types)


