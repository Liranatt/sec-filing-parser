from edgar.core import quarters_in_year
from sec_edgar_downloader import Downloader
from edgar import *
import pandas as pd
import csv
import os
import time
from pathlib import Path
"""set_identity("liranatt@post.bgu.ac.il")
company = Company("AAPL")
financials = company.get_financials()
income_statement_df = financials.income_statement().to_dataframe(include_dimensions=False)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.drop(columns=['concept', 'abstract', 'level', 'dimension', 'balance', 'weight', 'preferred_sign'])
    
    return clean_df

csv_filename =  'aaple_income_statement.csv'
clean_data(income_statement_df).to_csv(csv_filename, index=False)

"""

set_identity("liranatt@post.bgu.ac.il")
def get_data_using_edgar(companies_list: list[str]):
    NUMBER_OF_PERIODS = 25
    for company in companies_list:
        income_statement_df = Company(company).income_statement(
            periods=NUMBER_OF_PERIODS,
            annual=True,
            as_dataframe=True
        )
        clean_income_statement = income_statement_df.drop(columns=['is_abstract', 'is_total','section'])
        cash_flow_df = Company(company).cash_flow(
            periods=NUMBER_OF_PERIODS,
            annual=True,
            as_dataframe=True
        )
        clean_cash_flow = cash_flow_df.drop(columns=['is_abstract', 'is_total','section'])

        balance_sheet_df = Company(company).balance_sheet(
            periods=NUMBER_OF_PERIODS,
            annual=True,
            as_dataframe=True
        )
        clean_balance_sheet = balance_sheet_df.drop(columns=['is_abstract', 'is_total','section'])

        if not os.path.exists(f"{company}"):
            Path(f"{company}").mkdir()
        income_statement_csv = f'{company}/{company}_income_statement.csv'
        cash_flow_csv = f'{company}/{company}_cash_flow.csv'
        balance_sheet_csv = f'{com pany}/{company}_balance_sheet.csv'
        clean_income_statement.to_csv(income_statement_csv, index=False)
        clean_cash_flow.to_csv(cash_flow_csv, index=False)
        clean_balance_sheet.to_csv(balance_sheet_csv, index=False)
        time.sleep(1)



get_data_using_edgar(['AAPL', 'MSFT', 'GOOG'])

