import json
import pandas as pd
import tifffile
import numpy as np
from cached_property import cached_property

FOLDER = "/Users/edmz/data/icm_data/"
PATH_JSONL_LAST = "/doumazane/icm_toolbox/icm_toolbox/resources/atlas_last.jsonl"
PATH_JSONL_CLEARMAP = "/doumazane/icm_toolbox/icm_toolbox/resources/atlas_clearmap.jsonl"
PATH_TIFF_CLEARMAP = '/home/etienne.doumazane/code/ChristophKirst/ClearMap2/ClearMap/Resources/Atlas/ABA_25um_annotation.tif'
PATH_TIFF_2017 = '/Users/edmz/data/icm_data/atlas/atlas_tif/annotation_25_2017.tif'
# FOLDER = "/Users/edmz/data/icm_data/"
# PATH_JSONL_LAST = "/Users/edmz/data/icm_data/atlas_last.jsonl"
# PATH_JSONL_CLEARMAP = "../resources/atlas_clearmap.jsonl"
# PATH_TIFF_CLEARMAP = '/Users/edmz/data/icm_data/atlas/atlas_tif/annotation_25_clearmap.tif'
# PATH_TIFF_2017 = '/Users/edmz/data/icm_data/atlas/atlas_tif/annotation_25_2017.tif'



class Atlas:
    def __init__(self, tiff_version="2016", json_version="clearmap"):
        self.tiff_version = tiff_version
        self.json_version = json_version

    @cached_property
    def df(self):
        if self.json_version == "last":
            path_jsonl = PATH_JSONL_LAST
        elif self.json_version == "clearmap":
            path_jsonl = PATH_JSONL_CLEARMAP
        else:
            return
        return pd.read_json(path_jsonl, lines=True, orient="records")

    @cached_property
    def tiff(self):
        if self.tiff_version == "clearmap":
            path_tiff = PATH_TIFF_CLEARMAP
        elif self.tiff_version == "2017":
            path_tiff = PATH_TIFF_2017
        return tifffile.imread(path_tiff).astype(int)

    @cached_property
    def list_annotations(self):
        return np.unique(self.tiff)

    ###### maps from ids to names, acronyms...

    def get_map_to(self, col_name):
        return dict(zip(self.df['id'], self.df[col_name]))

    @cached_property
    def map_names(self):
        return self.get_map_to('name')

    @cached_property
    def map_acronyms(self):
        return self.get_map_to('acronym')

    ###### maps from ... to ids

    def get_map_from(self, col_name):
        return dict(zip(self.df[col_name], self.df['id']))

    @cached_property
    def map_acronym_to_id(self):
        return self.get_map_from('acronym')

    @cached_property
    def map_name_to_id(self):
        return self.get_map_from('name')


    def get_names(self, ids):
        return [self.map_names[id_] for id_ in ids]

    @cached_property
    def get_acronyms(self, ids):
        return [self.map_acronyms[id_] for id_ in ids]

    def get_map_children(self, parents_ids=None, including_parents=False):
        map_children = {}
        for parent_id in parents_ids:
            map_children[parent_id] = self.df.set_index('id').loc[parent_id, 'all_children_structures_ids'].copy()
        if including_parents:
            for parent in parents_ids:
                map_children[parent].append(parent)
        return map_children

    def get_map_parents(self, parents_ids=None, including_parents=False):
        map_children = self.get_map_children(parents_ids=parents_ids, including_parents=including_parents).copy()
        map_parent = {}
        for parent in map_children:
            for child in map_children[parent].copy():
                map_parent[child] = parent
        return map_parent

    def get_map_to_parent(self, parent_ids):
        """
        uses annotation graph to map all possible children structures to its parent in parent_ids
        """
        return self.get_map_parents(parent_ids, including_parents=True)

    def get_children(self, structure_ids):
        if isinstance(structure_ids, int):
            structure_ids = [structure_ids]
        map_children = self.get_map_children(parents_ids=structure_ids, including_parents=False)
        children = []
        for parent in map_children:
            children.extend(map_children[parent])
        return children

    def enrich_df(self, df):
        df = df.copy()
        df['name'] = df['id'].map(self.map_names)
        df['acronym'] = df['id'].map(self.map_acronyms)
        return df

def create_atlas_df(path, filter_cols=True, ):
    # read JSON file and create universe,
    # which is the master dictionary containing all structures, nested
    # dict obtained with
    # import requests
    # json = requests.get('http://api.brain-map.org/api/v2/structure_graph_download/1.json').json()['msg'][0]

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
