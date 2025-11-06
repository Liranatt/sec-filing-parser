# Imports for SEC data retrieval, data manipulation, and OS operations
from edgar.core import quarters_in_year
from sec_edgar_downloader import Downloader
from edgar import *
import pandas as pd
import csv
import os
import time
from pathlib import Path

"""
# DEV NOTE: Old test block for pulling a single company's data.
set_identity("liranatt@post.bgu.ac.il")
company = Company("AAPL")
financials = company.get_financials()
income_statement_df = financials.income_statement().to_dataframe(include_dimensions=False)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.drop(columns=['concept', 'abstract', 'level', 'dimension', 'balance', 'weight', 'preferred_sign'])
    
    return clean_df

csv_filename =  'aaple_income_statement.csv'
clean_data(income_statement_df).to_csv(csv_filename, index=False)

"""

# SEC EDGAR requires a user-agent string (email) for API access.
set_identity("liranatt@post.bgu.ac.il")

def get_data_using_edgar(companies_list: list[str]):
    """
    Iterates a list of company tickers, downloads key financial statements
    (Income, Cash Flow, Balance Sheet) for each, cleans them, and saves
    them to company-specific subdirectories.
    """
    
    # Define report depth: 25 years of annual data.
    NUMBER_OF_PERIODS = 25
    
    for company in companies_list:
        
        # Fetch annual income statement
        income_statement_df = Company(company).income_statement(
            periods=NUMBER_OF_PERIODS,
            annual=True,        # Request annual reports (not quarterly)
            as_dataframe=True   # Get a pandas DataFrame directly
        )
        # Drop metadata columns we don't need for this analysis
        clean_income_statement = income_statement_df.drop(columns=['is_abstract', 'is_total', 'section'])
        
        # Fetch annual cash flow statement
        cash_flow_df = Company(company).cash_flow(
            periods=NUMBER_OF_PERIODS,
            annual=True,
            as_dataframe=True
        )
        clean_cash_flow = cash_flow_df.drop(columns=['is_abstract', 'is_total', 'section'])

        # Fetch annual balance sheet
        balance_sheet_df = Company(company).balance_sheet(
            periods=NUMBER_OF_PERIODS,
            annual=True,
            as_dataframe=True
        )
        clean_balance_sheet = balance_sheet_df.drop(columns=['is_abstract', 'is_total', 'section'])

        # --- File Storage ---
        # Ensure a directory exists for the company's reports
        if not os.path.exists(f"{company}"):
            Path(f"{company}").mkdir()
            
        # Define output paths
        income_statement_csv = f'{company}/{company}_income_statement.csv'
        cash_flow_csv = f'{company}/{company}_cash_flow.csv'
        # Fixed typo: 'com pany' -> 'company'
        balance_sheet_csv = f'{company}/{company}_balance_sheet.csv'
        
        # Write dataframes to CSV, dropping the pandas index
        clean_income_statement.to_csv(income_statement_csv, index=False)
        clean_cash_flow.to_csv(cash_flow_csv, index=False)
        clean_balance_sheet.to_csv(balance_sheet_csv, index=False)
        
        # Be a good steward: rate limit requests to the SEC API.
        time.sleep(1)


# --- Execution ---
# Define the target companies and run the download function
get_data_using_edgar(['AAPL', 'MSFT', 'GOOG'])
