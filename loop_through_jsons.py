from pathlib import Path
import json
import using_company_facts
import pandas as pd
import re
folder_path = Path('companyfacts')
if not folder_path.is_dir():
    print("error")
else:
    for json_file in folder_path.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            print("json is empty")
            continue
        if not data.keys():
            print(data)
        print(data.keys())
        if 'cik' in data.keys():
            print(data['cik'])
        print(data['entityName'])
        translation_table = str.maketrans('','', "\/*,")
        entity_name = data['entityName'].translate(translation_table)
        csv_name = f'all_csv/{entity_name}.csv'
        wide_df = using_company_facts.wide_df(using_company_facts.flatten_financial_json(data))
        if wide_df.empty:
            continue
        wide_df.to_csv(csv_name, index=False)
        print(f"successfully created a csv for {csv_name}")
