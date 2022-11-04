import pandas as pd

def count_cells(path: str) -> pd.DataFrame:
    """
    counts cells from one file of type cells.feather
    returns df with columns id, hemisphere, cell_count and one row per structure x hemisphere
    """
    df = pd.read_feather(path)
    df['hemisphere'] = df['hemisphere'].map({0: 'LH', 255: 'RH'})
    counts = (df.groupby(['id', 'hemisphere'], as_index=False)
              .agg(cell_count=('name', 'count'))
              )
    counts = counts.reset_index(drop=True)
    return counts

def group_counts(counts_s, sample_names) -> pd.DataFrame:
    """
    groups several cell_counts together; sample_names are the names of the samples
    returns df with columns id, hemisphere, and one column per sample
    """
    counts_s = [counts.set_index(['id', 'hemisphere']) for counts in counts_s]
    df = pd.concat(counts_s, axis=1).fillna(0)
    df.columns = sample_names
    df = df.reset_index()
    return df

def collapse_structures(df: pd.DataFrame, map_collapse) -> pd.DataFrame:
    """
    collapses structures according to a dict map_collapse (id -> new_id)
    ids not in map_collapse are kept
    """
    df['id'] = df['id'].map(lambda x: map_collapse.get(x, x))
    counts = (df.groupby(['id', 'hemisphere'], as_index=False)
              .sum()
              )
    return counts

def filter_df(df: pd.DataFrame, structure_ids,
              hemispheres=['RH', 'LH'], exclude: bool=False) -> pd.DataFrame:
    """
    returns a df that includes only the
    """
    if exclude is False:
        df = df.loc[df["id"].isin(structure_ids) & df["hemisphere"].isin(hemispheres)].reset_index(drop=True)
        return df.copy()
    else:
        df = df.loc[~(df["id"].isin(structure_ids) & df["hemisphere"].isin(hemispheres))].reset_index(drop=True)
        return df.copy()

def normalize_df(df: pd.DataFrame, df_normalize: pd.DataFrame) -> pd.DataFrame:
    df = df.set_index(['id', 'hemisphere']).copy()
    df_normalize = df_normalize.set_index(['id', 'hemisphere']).copy()
    normalize_100 = df_normalize.sum(axis=0)
    df = df/normalize_100 * 100
    return df.reset_index()

