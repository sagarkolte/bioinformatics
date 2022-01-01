import pandas as pd
import numpy as np
import json
import os
from chembl_webresource_client.new_client import new_client

f = open('/Users/sagarkolte/Documents/Code/bioinformatics/config/data_prep_config.json', )
data = json.load(f)



def chembl_search(search_string):
    target = new_client.target
    target_query = target.search(search_string)
    targets = pd.DataFrame.from_dict(target_query)
    return targets


def get_bioactivity(target_chembl_id, standard_type):
    activity = new_client.activity
    res = activity.filter(target_chembl_id=target_chembl_id).filter(standard_type=standard_type)
    df = pd.DataFrame.from_dict(res)
    df = df[df.standard_value.notna()]
    return df


def main_pipe(target_chembl_id=data['target_chembl_id'], standard_type=data['standard_type']):
    df = get_bioactivity(target_chembl_id, standard_type)
    df['bioactivity_inactive'] = df['standard_value'].astype('float') >= 10000
    df['bioactivity_active'] = df['standard_value'].astype('float') < 1000
    df['bioactivity_intermediate'] = np.logical_not(np.logical_or(df['bioactivity_inactive'], df['bioactivity_active']))
    df = df[['molecule_chembl_id',
             'canonical_smiles',
             'standard_value',
             'bioactivity_inactive',
             'bioactivity_active',
             'bioactivity_intermediate']]
    df = df.drop_duplicates()
    df.to_csv(data["bioactivity_save_path"].format(target_chembl_id,standard_type))
    return None


