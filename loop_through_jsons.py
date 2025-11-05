""" 
    This file is responsible to loop throguh the jsons from facts after download from sec api: https://www.sec.gov/search-filings/edgar-application-programming-interfaces,
    from the bulk data part. after downloading you need to extract the facts folder and put the extracted folder into the project folder. 
     after that the file will loop throught the jsons, parse them and create csv's with the companies name and all the data that in the json
     (usually from 2009 till 2025 depends on the updates that has been done thorugh sec) 
"""



from pathlib import Path
import json
import using_company_facts
import pandas as pd
import re



""" part 1 confirming folder path """
folder_path = Path('companyfacts')
if not folder_path.is_dir():
    print("error")

else:
    """ part 2 loop through the json files """
    for json_file in folder_path.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        """printing data for easy check for errors"""
        if not data:
            print("json is empty")
            continue
            
        if not data.keys():
            print(data)

        print(data.keys())

        if 'cik' in data.keys():
            print(data['cik'])
            
        print(data['entityName'])
        
        """ removing characters that causes problems when trying to create the csv file """
        translation_table = str.maketrans('','', "\/*,")
        entity_name = data['entityName'].translate(translation_table)
        
        """ creating the path for the folders where all the csv's should be """
        csv_name = f'all_csv/{entity_name}.csv'
        
        """ getting the parsed data frame """ 
        wide_df = using_company_facts.wide_df(using_company_facts.flatten_financial_json(data))
        if wide_df.empty:
            continue
            
        """ creating the csv and put it in the folder """
        wide_df.to_csv(csv_name, index=False)
        print(f"successfully created a csv for {csv_name}")

