import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import pickle

if __name__ == "__main__":

    df = pd.read_csv('data/raw/train_short.csv')
    # df_majority = df[df['label'] == 'No']
    # df_minority = df[df['label'] == 'Yes']
    # df_majority_downsampled = resample(df_majority,
    #                                 replace=False,    
    #                                 n_samples=2*len(df_minority),
    #                                 random_state=42)
    # df_balanced = pd.concat([df_majority_downsampled, df_minority])

    X = df.drop(columns=['label'])
    y = df['label']        

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=27)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=27)

    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Exactitud del modelo: {accuracy}")
    print(classification_report(y_test, y_pred))

    with open('random_forest_model.pkl', 'wb') as file:
        pickle.dump(rf_model, file)

