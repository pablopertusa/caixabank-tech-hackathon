import pickle
import pandas as pd
import json

if __name__ == "__main__":
    
    with open('models/random_forest_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    with open('predictions/predictions_3.json', 'r') as f:
        pred = json.load(f)

    df = pd.read_csv('data/raw/transactions_data.csv')
    d_pred = {}
    for col in df.columns:
        d_pred[col] = []

    for id in pred['target']:
        for col in df.columns:
            d_pred[col].append(df[df['id'] == id][col].values)
    print(d_pred)

