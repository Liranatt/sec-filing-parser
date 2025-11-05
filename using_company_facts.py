"""
    this file job is to take the jsons and make them readable, he does that by turning them into a panda Data Frame where its easier to manipulate data
"""


import requests
import pandas as pd
import json
from pathlib import Path



""" for general knowledge to see what is inside the json files """
#print(data['facts'].keys())
#print(data['facts']['dei'].keys())

#print(data['facts']['us-gaap'].keys())
#print(data['facts']['srt'].keys())



def flatten_financial_json(json_data):
    """ 
        extracting data from the json's and putting them in an easy to read list full of easy to read dicitonaries and returning it as a panda Data Frame
    """
    
    all_facts = []
    
    if 'facts' not in json_data or 'us-gaap' not in json_data['facts']:
        print("could not find facts")
        return pd.DataFrame(all_facts)
        
    for concept_name, concept_data in json_data['facts']['us-gaap'].items():
        label = concept_data.get('label', 'Non label')

        for unit, data_points in concept_data.get('units', {}).items():
            for data_point in data_points:
                if 'val' not in data_point:
                    continue

                flat_fact = {
                    'label': label,
                    'concept_name': concept_name,
                    'unit': unit,
                    'value': data_point.get('val'),
                    'fiscal_year': data_point.get('fy'),
                    'fiscal_period': data_point.get('fp'),
                    'end_date': data_point.get('end'),
                    'form': data_point.get('form')
                }
                all_facts.append(flat_fact)

    return pd.DataFrame(all_facts)


def wide_df(long_df):
    """
        sorting the data
    """
    
    annual_forms = ['10-K', '10-K/A', '20-F', '20-F/A', '40-F', '40-F/A']
    
    if  long_df.empty or not 'form' in long_df.columns:
        return long_df
        
    annual_usd_df = long_df[
        (long_df['form'].isin(annual_forms)) &
        (long_df['unit'] == 'USD')
    ].copy()
    
    if annual_usd_df.empty:
        print("Warning: No annual USD data found.")
        return pd.DataFrame()
    """ sorting the data at the beginning by end data and dropping duplicates """    
    annual_usd_df.sort_values(by='end_date', ascending=True, inplace=True)
    annual_usd_df.drop_duplicates(subset=['label', 'fiscal_year'], keep='last', inplace=True)
    
    wide_df = annual_usd_df.pivot
    (
        index = 'label',
        columns ='fiscal_year',
        values='value'
    )

    cols_to_keep = [col for col in wide_df.columns if pd.notna(col)]
    wide_df = wide_df[cols_to_keep]

    wide_df.columns = [f"FY {int(col)}" for col in wide_df.columns]
    wide_df = wide_df.sort_index(axis=1, ascending=False)
    wide_df = wide_df.reset_index()
    wide_df.rename_axis(None, axis=1, inplace=True)
    wide_df.dropna(subset=['label'], inplace=True)
    return wide_df
"""
code for handling errors

path = Path('companyfacts/CIK0000850429.json')
with open(path, 'r') as f:
    data = json.load(f)
result_df = wide_df(flatten_financial_json(data))
print(result_df)
"""
