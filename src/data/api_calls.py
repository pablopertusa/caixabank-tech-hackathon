import pandas as pd
import requests
import time

if __name__ == "__main__":
    
    df = pd.read_csv("../../data/raw/transactions_data.csv")

    # card_data.csv
    resul = {}
    client_ids = df['client_id'].unique()
    cont = 0

    for client in client_ids:
        print(cont)
        r = requests.get('https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-a1f52b59-3551-477f-b8f3-de612fbf2769/default/cards-data', params = {'client_id': client}).json()
        if 'values' not in r:
            print('esperando')
            time.sleep(120)
            r = requests.get('https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-a1f52b59-3551-477f-b8f3-de612fbf2769/default/cards-data', params = {'client_id': client}).json()
            print(r)

        for card in r['values']:
            if len(resul) == 0:
                for col in r['values'][card]:
                    resul[col] = []
                resul['client_id'] = []
                resul['card_id'] = []
            for col in r['values'][card]:
                resul[col].append(r['values'][card][col])
            resul['card_id'].append(card)
        cont += 1

    df_cards = pd.DataFrame()
    for k in resul:
        df_cards[k] = resul[k]

    df_cards.to_csv('../../data/raw/card_data.csv')

    #client_data.csv
    resul2 = {}
    client_ids = df['client_id'].unique()
    cont = 0

    for client in client_ids:
        print(cont)
        r = requests.get('https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-a1f52b59-3551-477f-b8f3-de612fbf2769/default/clients-data', params = {'client_id': client}).json()
        if 'values' not in r:
            print('esperando')
            time.sleep(120)
            r = requests.get('https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-a1f52b59-3551-477f-b8f3-de612fbf2769/default/clients-data', params = {'client_id': client}).json()

        for col in r['values']:
            if len(resul2) == 0:
                for col2 in r['values']:
                    resul2[col2] = []
                resul2['client_id'] = []
            resul2[col].append(r['values'][col])
        resul2['client_id'].append(client)
        cont += 1
    
    df_clients = pd.DataFrame()
    for k in resul2:
        df_clients[k] = resul2[k]

    df_clients.to_csv('../../data/raw/client_data.csv')


