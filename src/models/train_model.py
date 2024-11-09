import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import pickle
import json

if __name__ == "__main__":

    with open('/home/pablo/Desktop/side/caixabank-tech-hackathon/data/raw/columns_datatypes.json', 'r') as f:
        types = json.load(f)
    df = pd.read_csv('/home/pablo/Desktop/side/caixabank-tech-hackathon/data/raw/train_downcasted.csv', dtype=types)

    X = df.drop(columns=['label'])
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=27)

    rf_model = RandomForestClassifier(n_estimators=20, random_state=27)

    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Exactitud del modelo: {accuracy}")
    print(classification_report(y_test, y_pred))

    with open('/home/pablo/Desktop/side/caixabank-tech-hackathon/models/random_forest_model.pkl', 'wb') as file:
        pickle.dump(rf_model, file)

