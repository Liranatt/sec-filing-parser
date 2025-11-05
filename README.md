# SEC EDGAR Financial Data Processor

Python tools for acquiring and processing SEC EDGAR financial data. scraping_edgar.py fetches income statements, balance sheets, and cash flow reports. loop_through_jsons.py & using_company_facts.py parse local company fact JSONs, filtering and pivoting annual financial data into wide-format CSVs.

Features

Fetch Financial Statements: Scrape annual income statements, balance sheets, and cash flow reports for a list of company tickers.

Parse Company Facts: Process the bulk JSON "company facts" files provided by the SEC.

Data Transformation: Flatten complex nested JSON data from the us-gaap section into a simple tabular format.

Pivot to Wide Format: Convert long-format financial data into a wide-format CSV (metrics as rows, fiscal years as columns) for easy analysis in Excel or Pandas.

Scripts Overview

This repository contains two main workflows:

scraping_edgar.py:

Uses the python-edgar library to connect to the EDGAR database.

Takes a list of company tickers (e.g., ['AAPL', 'MSFT', 'GOOG']).

Downloads the last 25 periods of annual financial statements (Income, Balance Sheet, Cash Flow).

Saves the cleaned data into per-company folders (e.g., AAPL/AAPL_income_statement.csv).

loop_through_jsons.py (with using_company_facts.py):

This workflow is designed to process the bulk "Company Facts" JSON files available from the SEC.

using_company_facts.py is a utility module that contains the core logic:

flatten_financial_json(data): Parses the nested us-gaap facts.

wide_df(long_df): Filters for annual (10-K, 20-F) reports in USD, de-duplicates, and pivots the data into a wide-format DataFrame.

loop_through_jsons.py is the main script that:

Looks for a local directory named companyfacts/.

Iterates through every .json file in that directory.

Applies the flattening and pivoting logic.

Saves a clean, wide-format CSV for each company into the all_csv/ directory.

Setup & Installation

Clone this repository:

git clone [https://github.com/YOUR_USERNAME/sec-edgar-processor.git](https://github.com/YOUR_USERNAME/sec-edgar-processor.git)
cd sec-edgar-processor


Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install the required Python libraries:

pip install pandas python-edgar


Create the output directories:

mkdir all_csv


Usage

You can use either workflow depending on your needs.

1. Scraping Financial Statements by Ticker

This method is best for getting standard financial statements for a few specific companies.

Open scraping_edgar.py.

Important: Set your email address for the EDGAR User-Agent, as required by the SEC.

set_identity("your-email@example.com")


Modify the list of companies in the last line of the script:

get_data_using_edgar(['AAPL', 'MSFT', 'GOOG'])


Run the script from your terminal:

python scraping_edgar.py


Your files will be saved in new directories named after the tickers (e.g., AAPL/, MSFT/).

2. Processing Bulk Company Fact JSONs

This method is for processing the bulk "Company Facts" JSON files, which can be downloaded from the SEC website.

Download the company fact JSON files you need (e.g., CIK0000320193.json for Apple).

Place all .json files into a directory named companyfacts/ in the root of this project.

Run the processing script from your terminal:

python loop_through_jsons.py


Cleaned, wide-format CSVs for each company will be saved in the all_csv/ directory (e.g., all_csv/APPLE INC.csv).

License

This project is licensed under the MIT License.
