import json
import pandas as pd

FOLDER = "/Users/edmz/data/icm_data/"


class Atlas:
    def __init__(self):
        self.df = pd.read_json(FOLDER + 'atlas_enriched.jsonl', lines=True)
        self.map_names = self.get_map_names()

    def get_map_children(self, parents_ids=None, including_parent=False):
        if parents_ids is None:
            parents_ids = self.df['id']
        children_ids = self.df.loc[self.df['id'].isin(parents_ids), 'all_children_structures_ids']
        map_children = dict(zip(parents_ids, children_ids))
        if including_parent:
            for parent in map_children.keys():
                map_children[parent].append(parent)
        return map_children

    def get_map_parents(self, parents_ids=None, including_parent=False):
        map_children = self.get_map_children(parents_ids=parents_ids, including_parent=including_parent)
        map_parent = {}
        for parent in map_children.keys():
            for child in map_children[parent]:
                map_parent[child] = parent
        return map_parent

    def get_map_names(self, ids=None):
        if ids is None:
            ids = self.df['id']
        names = self.df.loc[self.df['id'].isin(ids), 'name']
        map_names = dict(zip(ids, names))
        return map_names

    def get_map_acronyms(self, ids=None):
        if ids is None:
            ids = self.df['id']
        acronyms = self.df.loc[self.df['id'].isin(ids), 'acronym']
        map_acronyms = dict(zip(ids, acronyms))
        return map_acronyms

    def get_map_name_to_id(self):
        map_name_to_id = dict(zip(self.df['name'], self.df['id']))
        return map_name_to_id

    def get_children(self, structure_id):
        map_children = self.get_map_children()
        return map_children.get(structure_id)


def get_children_list(structure):
    """
    flatten any structure
    structure : dict
    """
    children_list = []
    children = structure.get('children')  # can be empty list
    for child in children:
        children_list.append(child)
        children_list.extend(get_children_list(child))  # recursion
    return children_list


def set_children_depth(children, depth) -> None:
    for child in children:
        child['depth'] = depth
        set_children_depth(child.get("children"), depth + 1)


def get_direct_children_structures_ids(children):
    """
    list the ids of direct children only
    """
    return [child.get("id") for child in children]

def get_all_children_structures_ids(children):
    """
    list the ids of direct children, their children and so on
    """
    list_all_children = children.copy()
    for child in children:
        list_all_children.extend(get_children_list(child))
    return [child.get("id") for child in list_all_children]


def create_atlas_df(path, filter_cols=True):
    # read JSON file and create universe,
    # which is the master dictionary containing all structures, nested
    with open(path) as file_in:
        annotation = json.load(file_in)
    universe = annotation['msg'][0]

    # create depth within universe
    set_children_depth([universe], -1)

    # flatten universe children
    children_of_universe = get_children_list(universe)
    df = pd.DataFrame(children_of_universe)

    if filter_cols:
        cols_of_interest = [
            'id',  # probably their primary key
            'atlas_id',  # probably the atlas reference id, some are null
            'acronym',
            'name',
            'color_hex_triplet',
            'graph_order',  # changes from one version to another
            'parent_structure_id',
            'children',
            'depth']
        df = df[cols_of_interest].copy()
    df["direct_children_structures_ids"] = df.children.map(get_direct_children_structures_ids)
    df['all_children_structures_ids'] = df.children.map(get_all_children_structures_ids)
    df['nb_direct_children'] = df.direct_children_structures_ids.map(len)
    df['nb_all_children'] = df.all_children_structures_ids.map(len)
    df['is_leaf'] = (df.nb_direct_children == 0)

    return df


def get_enriched_atlas_df(path):
    # FIXME

    # create new columns
    df = create_atlas_df(path)

    def get_parent(structure_id):
        parent_id = atlas_df.loc[atlas_df['id'] == structure_id, 'parent_structure_id']
        if parent_id.values.size:
            return parent_id.values[0]

    def get_all_parents(structure_id):
        all_parents = []
        parent_id = get_parent(structure_id)
        while parent_id:
            all_parents.append(parent_id)
            parent_id = get_parent(structure_id)
        return all_parents

    atlas_df = df.copy()
    df['all_parent_structures_ids'] = df.parent_structure_id.map(get_all_parents)
    return df


def get_atlas():
    atlas = pd.read_json(FOLDER + 'Atlas_annotation_ED.json')
    atlas = atlas[['name', 'id']].copy()
    atlas['hemisphere'] = 'LH'
    atlas['region_id'] = atlas['id']
    atlas_r = atlas.copy()
    atlas_r['hemisphere'] = 'RH'
    atlas_r['region_id'] = atlas_r['region_id'].map(lambda x: x + 100_000)
    atlas = pd.concat([atlas, atlas_r]).reset_index(drop=True)
    return atlas
