import pickle

if __name__ == "__main__":
    with open('random_forest_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    ind = []
