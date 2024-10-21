import pandas as pd


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

    return pd.DataFrame({"Earnings": [], "Expenses": []})


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

    return pd.DataFrame(
        {
            "Expenses Type": [],
            "Total Amount": [],
            "Average": [],
            "Max": [],
            "Min": [],
            "Num. Transactions": [],
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
    return pd.DataFrame()


if __name__ == "__main__":
    ...
