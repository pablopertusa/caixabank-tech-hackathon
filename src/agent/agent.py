from langchain_ollama import ChatOllama
import pandas as pd


def run_agent(df: pd.DataFrame, client_id: int, input: str) -> dict:
    """
    Create a simple AI Agent that generates PDF reports using the three functions from Task 2 (src/data/data_functions.py).
    The agent should generate a PDF report only if valid data is available for the specified client_id and date range.
    Using the data and visualizations from Task 2, the report should be informative and detailed.

    The agent should return a dictionary containing the start and end dates, the client_id, and whether the report was successfully created.

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame  of the data to be used for the agent.
    client_id : int
        Id of the client making the request.
    input : str
        String with the client input for creating the report.


    Returns
    -------
    variables_dict : dict
        Dictionary of the variables of the query.
            {
                "start_date": "YYYY-MM-DD",
                "end_date" : "YYYY-MM-DD",
                "client_id": int,
                "create_report" : bool
            }

    """
    tools = []
    model = ChatOllama(model="llama3.2:1b", temperature=0)
    pdf_output_folder = "reports/"
    # ---
    variables_dict = {
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "client_id": 0,
        "create_report": False,
    }

    return variables_dict


if __name__ == "__main__":
    ...
