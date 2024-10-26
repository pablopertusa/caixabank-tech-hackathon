import pandas as pd
from datetime import datetime
import json

def question_1(cards_df):

    """
    Q1: - The `card_id` with the latest expiry date and the lowest credit limit amount.
    """

    def fecha_a_numerico(f):
        m = f.split('/')[0]
        y = f.split('/')[1]
        resul = float(y) + float(m)/12
        return resul

    def max_expires(l):
        resul = []
        for x in l:
            resul.append(fecha_a_numerico(x))
        maximo = resul.index(max(resul))
        return maximo
    
    mayor_expires = cards_df.iloc[max_expires(cards_df['expires'].values),:]['expires']
    exp = cards_df[cards_df['expires'] == mayor_expires]
    x = list(exp['credit_limit'].map(lambda x: float(x[1:])).values)
    min = max(x)
    for i in x:
        if i < min:
            min = i
    min = int(min)
    resul = exp[exp['credit_limit'] == f'${min}']
    ret = resul['card_id'].values[0]
    return ret



def question_2(client_df):
    """
    Q2: - The `client_id` that will retire within a year that has the lowest credit score and highest debt.
    """
    def map_clients(list_edad, list_retirement):
        resul = []
        for i in range(len(list_edad)):
            if (int(list_retirement[i]) - int(list_edad[i])) == 1:
                resul.append(True)
            else:
                resul.append(False)
        return resul

    ret = client_df[map_clients(client_df['current_age'], client_df['retirement_age'])]
    resul = ret[ret['total_debt'] == max(ret['total_debt'].values)]['client_id'].values[0]
    return resul


def question_3(transactions_df):
    """
    Q3: - The `transaction_id` of an Online purchase on a 31st of December with the highest absolute amount (either earnings or expenses).
    """
    def ultimo_diciembre(s):
        d = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        if d.month == 12 and d.day == 31:
            return True
        return False
    dic = transactions_df[transactions_df['date'].map(ultimo_diciembre)]
    resul = dic[dic['amount'] == '$'+str(max(dic['amount'].map(lambda x: abs(float(x[1:])))))]
    r = resul['id'].values[0]
    return r



def question_4(client_df, cards_df, transactions_df):
    """
    Q4: - Which client over the age of 40 made the most transactions with a Visa card in February 2016?
    Please return the `client_id`, the `card_id` involved, and the total number of transactions.
    """
    def febrero_2016(s):
        d = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        if d.month == 2 and d.year == 2016:
            return True
        return False

    mayores = client_df[client_df['current_age'] > 40]
    visa = cards_df[cards_df['card_brand'] == 'Visa']
    febrero = transactions_df[transactions_df['date'].map(febrero_2016)]
    merged1 = pd.merge(mayores, visa, how='inner', on='client_id')
    merged2 = pd.merge(merged1, febrero, how='inner', on='card_id')

    cont = {}
    for _, row in merged2.iterrows():
        client = row['client_id_x']
        card = row['card_id']
        if (client, card) not in cont:
            cont[(client, card)] = 1
        else:
            cont[(client, card)] += 1
    max_cont = 0
    max_id = None
    for tupla in cont:
        if cont[tupla] > max_cont:
            max_id = tupla
            max_cont = cont[tupla]
    max_client = max_id[0]
    max_card = max_id[1]
    return max_client, max_card, max_cont


if __name__ == "__main__":
    cards_df = pd.read_csv("data/raw/card_data.csv")
    client_df = pd.read_csv("data/raw/client_data.csv")
    transactions_df = pd.read_csv("data/raw/transactions_data.csv")
    q1 = question_1(cards_df)
    q2 = question_2(client_df)
    q3 = question_3(transactions_df)
    q4_1, q4_2, q4_3 = question_4(client_df, cards_df, transactions_df)

    resultado_1 = {
        "target": {
            "query_1": {
                "card_id": int(q1)
            },
            "query_2": {
                "client_id": int(q2)
            },
            "query_3": {
                "transaction_id": int(q3)
            },
            "query_4": {
                "client_id": int(q4_1),
                "card_id": int(q4_2),
                "number_transactions": int(q4_3)
            }
        }
    }
    with open("predictions/predictions_1_res.json", "w") as archivo:
        json.dump(resultado_1, archivo, indent=4)