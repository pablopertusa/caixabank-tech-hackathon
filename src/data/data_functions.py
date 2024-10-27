import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json

def earnings_and_expenses(
    df: pd.DataFrame, client_id: int, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    For the period defined in between start_date and end_date (both included), get the client data available and return
    a pandas DataFrame with the Earnings and Expenses total amount for the period range and user given.The expected columns are:
        - Earnings
        - Expenses
    The DataFrame should have the columns in this order ['Earnings','Expenses']. Round the amounts to 2 decimals.

    Create a Bar Plot with the Earnings and Expenses absolute values and save it as "reports/figures/earnings_and_expenses.png" .

    Parameters
    ----------
    df : pandas DataFrame
       DataFrame of the data to be used for the agent.
    client_id : int
        Id of the client.
    start_date : str
        Start date for the date period. In the format "YYYY-MM-DD".
    end_date : str
        End date for the date period. In the format "YYYY-MM-DD".


    Returns
    -------
    Pandas Dataframe with the earnings and expenses rounded to 2 decimals.

    """

    def estar_entre(start, end, x):
        if start <= x and end >= x:
            return True
        return False
    
    earnings = 0
    expenses = 0
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    select1 = df[df['client_id'] == client_id]
    select2 = select1[select1['date'].map(lambda x: estar_entre(start_date, end_date, x))]
    for _, row in select2.iterrows():
        amount = row['amount']
        if float(amount[1:]) < 0:
            expenses += float(amount[1:])
        else:
            earnings += float(amount[1:])

    earnings = round(earnings, 2)
    expenses = round(expenses, 2)

    fig, ax = plt.subplots()
    categories = ['Earnings', 'Expenses']
    values = [earnings, expenses]
    ax.bar(categories, values)
    ax.set_ylabel('Amount')
    ax.set_title('Earnings and Expenses')

    output_dir = "reports/figures"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "earnings_and_expenses.png"), format='png', dpi=300)

    return pd.DataFrame({"Earnings": [earnings], "Expenses": [expenses]})


def expenses_summary(
    df: pd.DataFrame, client_id: int, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    For the period defined in between start_date and end_date (both included), get the client data available and return
    a Pandas Data Frame with the Expenses by merchant category. The expected columns are:
        - Expenses Type --> (merchant category names)
        - Total Amount
        - Average
        - Max
        - Min
        - Num. Transactions
    The DataFrame should be sorted alphabeticaly by Expenses Type and values have to be rounded to 2 decimals. Return the dataframe with the columns in the given order.
    The merchant category names can be found in data/raw/mcc_codes.json .

    Create a Bar Plot with the data in absolute values and save it as "reports/figures/expenses_summary.png" .

    Parameters
    ----------
    df : pandas DataFrame
       DataFrame  of the data to be used for the agent.
    client_id : int
        Id of the client.
    start_date : str
        Start date for the date period. In the format "YYYY-MM-DD".
    end_date : str
        End date for the date period. In the format "YYYY-MM-DD".


    Returns
    -------
    Pandas Dataframe with the Expenses by merchant category.

    """

    def estar_entre(start, end, x):
        #x = datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')
        if start <= x and end >= x:
            return True
        return False

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    select1 = df[df['client_id'] == client_id]
    select2 = select1[select1['date'].map(lambda x: estar_entre(start_date, end_date, x))]
    print(len(select2))

    categorias = set(select2['mcc'].values)
    d = {}

    with open('data/raw/mcc_codes.json', 'r') as file:
        dict_categorias = json.load(file)

    for cat in categorias:
        df_cat = select2[select2['mcc'] == cat]
        df_cat['amount'] = df_cat['amount'].map(lambda x: float(x[1:]))
        total = round(sum(df_cat['amount'].values),2)
        avg = round(total/len(df_cat['amount'].values),2)
        n_transactions = len(df_cat['amount'].values)
        minimo = round(min(df_cat['amount'].values),2)
        maximo = round(max(df_cat['amount'].values),2)
        categoria = dict_categorias[str(cat)]
        d[categoria] = {
            'Total Amount': total,
            'Average': avg,
            'Max': maximo,
            'Min': minimo,
            'Num. Transactions': n_transactions
        }
    

    ordenadas = sorted([dict_categorias[str(c)] for c in categorias])
    expenses_type = []
    total_amount = []
    average = []
    maximo_l = []
    minimo_l = []
    num_transactions = []

    for c in ordenadas:
        if c in d:
            expenses_type.append(c)
            total_amount.append(d[c]['Total Amount'])
            average.append(d[c]['Average'])
            maximo_l.append(d[c]['Max'])
            minimo_l.append(d[c]['Min'])
            num_transactions.append(d[c]['Num. Transactions'])

    df_result = pd.DataFrame(
        {
            "Expenses Type": expenses_type,
            "Total Amount": total_amount,
            "Average": average,
            "Max": maximo,
            "Min": minimo,
            "Num. Transactions": num_transactions,
        }
    )
    _, ax = plt.subplots()
    ax.bar(df_result['Expenses Type'], df_result['Total Amount'])
    ax.set_ylabel('Total Amount')
    ax.set_title('Expenses by Merchant Category')
    plt.xticks(rotation=90)
    
    output_dir = "reports/figures"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "expenses_summary.png"))
    plt.close()


    return pd.DataFrame(
        {
            "Expenses Type": expenses_type,
            "Total Amount": total_amount,
            "Average": average,
            "Max": maximo,
            "Min": minimo,
            "Num. Transactions": num_transactions,
        }
    )


def cash_flow_summary(
    df: pd.DataFrame, client_id: int, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    For the period defined by start_date and end_date (both inclusive), retrieve the available client data and return a Pandas DataFrame containing cash flow information.

    If the period exceeds 60 days, group the data by month, using the end of each month for the date. If the period is 60 days or shorter, group the data by week.

        The expected columns are:
            - Date --> the date for the period. YYYY-MM if period larger than 60 days, YYYY-MM-DD otherwise.
            - Inflows --> the sum of the earnings (positive amounts)
            - Outflows --> the sum of the expenses (absolute values of the negative amounts)
            - Net Cash Flow --> Inflows - Outflows
            - % Savings --> Percentage of Net Cash Flow / Inflows

        The DataFrame should be sorted by ascending date and values rounded to 2 decimals. The columns should be in the given order.

        Parameters
        ----------
        df : pandas DataFrame
           DataFrame  of the data to be used for the agent.
        client_id : int
            Id of the client.
        start_date : str
            Start date for the date period. In the format "YYYY-MM-DD".
        end_date : str
            End date for the date period. In the format "YYYY-MM-DD".


        Returns
        -------
        Pandas Dataframe with the cash flow summary.

    """

    def estar_entre(start, end, x):
        if start <= x and end >= x:
            return True
        return False
    
    def quitar_nan(x):
        if str(x) == 'nan':
            return 0
        return x

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    select1 = df[df['client_id'] == client_id]
    select2 = select1[select1['date'].map(lambda x: estar_entre(start_date, end_date, x))]

    days_between = (end_date-start_date).days

    if days_between > 60:
        select2['amount'] = select2['amount'].map(lambda x: float(x[1:]))
        expenses = select2[select2['amount'] < 0]
        earnings = select2[select2['amount'] > 0]
        expenses.set_index('date', inplace=True)
        df_semanal_expenses = expenses.resample('M').sum()
        earnings.set_index('date', inplace=True)
        df_semanal_earning = earnings.resample('M').sum()
        resul = pd.DataFrame({
            'Date': df_semanal_earning.index,
            'Inflows': df_semanal_earning['amount'],
            'Outflows': df_semanal_expenses['amount'],
        }
        )
        resul['Inflows'] = resul['Inflows'].map(quitar_nan)
        resul['Outflows'] = resul['Outflows'].map(lambda x: abs(quitar_nan(x)))

        resul['Net Cash Flow'] = resul['Inflows'] - resul['Outflows']
        resul['% Savings'] = (resul['Net Cash Flow']*100/resul['Inflows']).map(lambda x: round(x,2))
        resul['Date'] = resul['Date'].map(lambda x: datetime.strftime(x, '%Y-%m'))

    else:
        select2['amount'] = select2['amount'].map(lambda x: float(x[1:]))
        expenses = select2[select2['amount'] < 0]
        earnings = select2[select2['amount'] > 0]
        expenses.set_index('date', inplace=True)
        df_semanal_expenses = expenses.resample('W').sum()
        earnings.set_index('date', inplace=True)
        df_semanal_earning = earnings.resample('W').sum()
        resul = pd.DataFrame({
            'Date': df_semanal_earning.index,
            'Inflows': df_semanal_earning['amount'],
            'Outflows': df_semanal_expenses['amount'],
        }
        )
        resul['Inflows'] = resul['Inflows'].map(quitar_nan)
        resul['Outflows'] = resul['Outflows'].map(lambda x: abs(quitar_nan(x)))

        resul['Net Cash Flow'] = resul['Inflows'] - resul['Outflows']
        resul['% Savings'] = (resul['Net Cash Flow']*100/resul['Inflows']).map(lambda x: round(x,2))
        resul['Date'] = resul['Date'].map(lambda x: datetime.strftime(x, '%Y-%m-%d'))



    resul.index = pd.RangeIndex(start=0, stop=len(resul), step=1)
    return resul


if __name__ == "__main__":
    ...
