import os

import pandas as pd

from my_package.atlas import Atlas

def count_cells_by_structure(path):
    """takes feather path"""
    df = pd.read_feather(path)
    df['hemisphere'] = df['hemisphere'].map({0: 'RH', 255: 'LH'})  # CHECKME
    counts = (df.groupby(['id', 'hemisphere'], as_index=False)
              .agg(cell_count=('name', 'count'))
              )
    counts = counts.sort_values(by='cell_count', ascending=False).reset_index(drop=True)
    return counts

def enrich_df(df):
    atlas = Atlas()
    map_names = atlas.get_map_names()
    map_acronyms = atlas.get_map_acronyms()
    df = df.copy()
    df['name'] = df['id'].map(map_names)
    df['acronym'] = df['id'].map(map_acronyms)
    return df

def get_multiple_counts(counts_s, colnames):
    counts_s = [counts.set_index(['id', 'hemisphere']) for counts in counts_s]
    table = pd.concat(counts_s, axis=1).fillna(0)
    table.columns = colnames
    table = table.reset_index()
    return table


def pool_structures_by_parent_structure(structure_id):
    """
    take a df
    """


if __name__ == "__main__":
    FOLDER = '/Users/edmz/data/icm_data/bulk/RFP_5_months/'
    path = FOLDER + os.listdir(FOLDER)[0]
    print(count_cells_by_structure(path))
