# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/spec_lib/translate.ipynb (unless otherwise specified).

__all__ = ['create_modified_sequence', 'merge_precursor_fragment_df', 'mask_fragment_intensity_by_mz_',
           'speclib_to_single_df', 'mod_to_other_mod_dict', 'mod_to_unimod_dict']

# Cell
import pandas as pd
import numpy as np
import tqdm
import typing
import itertools

from alphabase.spectrum_library.library_base import SpecLibBase
from peptdeep.model.ccs import ccs_to_mobility_pred_df

# Cell
#@numba.njit #(cannot use numba for pd.Series)
def create_modified_sequence(
    df_items:typing.Tuple, # must be ('sequence','mods','mod_sites')
    translate_mod_dict:dict=None,
    mod_sep='[]'
):
    '''
    Translate `(sequence, mods, mod_sites)` into a modified sequence. Used by `df.apply()`.
    For example, `('ABCDEFG','Mod1@A;Mod2@E','1;5')`->`_A[Mod1@A]BCDE[Mod2@E]FG_`.
    Args:
        df_items (List): must be `(sequence, mods, mod_sites)`
        translate_mod_dict (dict): A dict to map alpha modification names to other software
        mod_seq (str): '[]' or '()', default '[]'
    '''
    nterm = '_'
    cterm = '_'
    mod_seq = df_items[0]
    if df_items[1]:
        mods = df_items[1].split(';')[::-1]
        mod_sites = df_items[2].split(';')[::-1]
        if translate_mod_dict is not None:
            mods = [translate_mod_dict[mod] for mod in mods]
        for site, mod in zip(mod_sites, mods):
            _site = int(site)
            if _site > 0:
                mod_seq = mod_seq[:_site] + mod_sep[0]+mod+mod_sep[1] + mod_seq[_site:]
            elif _site == -1:
                cterm += mod_sep[0]+mod+mod_sep[1]
            elif _site == 0:
                nterm += mod_sep[0]+mod+mod_sep[1]
            else:
                mod_seq = mod_seq[:_site] + mod_sep[0]+mod+mod_sep[1] + mod_seq[_site:]
    return nterm + mod_seq + cterm

# Cell

def _get_frag_info_from_column_name(column:str):
    '''
    Only used when convert alphabase libraries into other libraries
    '''
    idx = column.rfind('_')
    frag_type = column[:idx]
    ch_str = column[idx+2:]
    charge = int(ch_str)
    if len(frag_type)==1:
        loss_type = 'noloss'
    else:
        idx = frag_type.find('_')
        loss_type = frag_type[idx+1:]
        frag_type = frag_type[0]
    return frag_type, loss_type, charge

def _get_frag_num(columns, rows, frag_len):
    frag_nums = []
    for r,c in zip(rows, columns):
        if c[0] in 'xyz':
            frag_nums.append(frag_len-r)
        else:
            frag_nums.append(r+1)
    return frag_nums

def _flatten(list_of_lists):
    '''
    Flatten a list of lists
    '''
    return list(
        itertools.chain.from_iterable(list_of_lists)
    )

def merge_precursor_fragment_df(
    precursor_df:pd.DataFrame,
    fragment_mz_df:pd.DataFrame,
    fragment_inten_df:pd.DataFrame,
    top_n_inten:int,
    frag_type_head:str='FragmentType',
    frag_mass_head:str='FragmengMz',
    frag_inten_head:str='RelativeIntensity',
    frag_charge_head:str='FragmentCharge',
    frag_loss_head:str='FragmentLossType',
    frag_num_head:str='FragmentNumber'
):
    '''
    Convert alphabase library into a single dataframe.
    This method is not important, as it will be only
    used by DiaNN, or spectronaut, or others
    '''
    df = precursor_df.copy()
    frag_columns = fragment_mz_df.columns.values.astype('U')
    frag_type_list = []
    frag_loss_list = []
    frag_charge_list = []
    frag_mass_list = []
    frag_inten_list = []
    frag_num_list = []
    for start, end in tqdm.tqdm(df[['frag_start_idx','frag_end_idx']].values):
        intens = fragment_inten_df.iloc[start:end,:].values # is loc[start:end-1,:] faster?
        masses = fragment_mz_df.iloc[start:end,:].values
        sorted_idx = np.argsort(intens.reshape(-1))[-top_n_inten:][::-1]
        idx_in_df = np.unravel_index(sorted_idx, masses.shape)

        frag_len = end-start
        rows = np.arange(frag_len, dtype=np.int32)[idx_in_df[0]]
        columns = frag_columns[idx_in_df[1]]

        frag_types, loss_types, charges = zip(
            *[_get_frag_info_from_column_name(_) for _ in columns]
        )

        frag_nums = _get_frag_num(columns, rows, frag_len)

        frag_type_list.append(frag_types)
        frag_loss_list.append(loss_types)
        frag_charge_list.append(charges)
        frag_mass_list.append(masses[idx_in_df])
        frag_inten_list.append(intens[idx_in_df])
        frag_num_list.append(frag_nums)

    try:
        df[frag_type_head] = frag_type_list
        df[frag_mass_head] = frag_mass_list
        df[frag_inten_head] = frag_inten_list
        df[frag_charge_head] = frag_charge_list
        df[frag_loss_head] = frag_loss_list
        df[frag_num_head] = frag_num_list
        return df.explode([
            frag_type_head,
            frag_mass_head,
            frag_inten_head,
            frag_charge_head,
            frag_loss_head,
            frag_num_head
        ])
    except ValueError:
        # df.explode does not allow mulitple columns before pandas version 1.x.x.
        df[frag_type_head] = frag_type_list
        df = df.explode(frag_type_head)

        df[frag_mass_head] = _flatten(frag_mass_list)
        df[frag_inten_head] = _flatten(frag_inten_list)
        df[frag_charge_head] = _flatten(frag_charge_list)
        df[frag_loss_head] = _flatten(frag_loss_list)
        df[frag_num_head] = _flatten(frag_num_list)
        return df

mod_to_other_mod_dict = {
    "Carbamidomethyl@C": "Carbamidomethyl (C)",
    "Oxidation@M": "Oxidation (M)",
    "Phospho@S": "Phospho (STY)",
    "Phospho@T": "Phospho (STY)",
    "Phospho@Y": "Phospho (STY)",
    "GlyGly@K": "GlyGly (K)",
    "Acetyl@Protein N-term": "Acetyl (Protein N-term)",
}

from alphabase.constants.modification import MOD_DF
mod_to_unimod_dict = {}
for mod_name,unimod_id in MOD_DF[['name','unimod_id']].values:
    mod_to_unimod_dict[mod_name] = f"UniMod:{unimod_id}"

def mask_fragment_intensity_by_mz_(
    fragment_mz_df:pd.DataFrame,
    fragment_intensity_df:pd.DataFrame,
    min_frag_mz, max_frag_mz
):
    fragment_intensity_df.mask(
        (fragment_mz_df>max_frag_mz)&(fragment_mz_df<min_frag_mz),
        0, inplace=True
    )

def speclib_to_single_df(
    speclib:SpecLibBase,
    *,
    translate_mod_dict:dict = None,
    keep_k_highest_intensity:int=12,
    modloss='H3PO4',
    frag_type_head:str='FragmentType',
    frag_mass_head:str='FragmentMz',
    frag_inten_head:str='RelativeIntensity',
    frag_charge_head:str='FragmentCharge',
    frag_loss_head:str='FragmentLossType',
    frag_num_head:str='FragmentNumber',
    min_frag_mz = 200,
    max_frag_mz = 2000,
    min_frag_intensity = 0.02,
):
    '''
    Convert alphabase library to diann (or Spectronaut) library dataframe
    This method is not important, as it will be only
    used by DiaNN, or spectronaut, or others
    Args:
        translate_mod_dict (dict): a dict map modifications from alphabase to other software. Default: build-in `alpha_to_other_mod_dict`
        keep_k_highest_intensity (int): only keep highest fragment intensities for each precursor. Default: 12
    Returns:
        pd.DataFrame: a single-file dataframe which contains precursors and fragments
    '''
    df = pd.DataFrame()
    df['ModifiedPeptide'] = speclib._precursor_df[
        ['sequence','mods','mod_sites']
    ].apply(
        create_modified_sequence,
        axis=1,
        translate_mod_dict=translate_mod_dict,
        mod_sep='[]'
    )

    df['frag_start_idx'] = speclib._precursor_df['frag_start_idx']
    df['frag_end_idx'] = speclib._precursor_df['frag_end_idx']

    df['PrecursorCharge'] = speclib._precursor_df['charge']
    if 'rt_pred' in speclib._precursor_df.columns:
        df['iRT'] = speclib._precursor_df['rt_pred']
    elif 'rt_norm' in speclib._precursor_df.columns:
        df['iRT'] = speclib._precursor_df['rt_norm']
    else:
        raise ValueError('precursor_df must contain the "rt_pred" or "rt_norm" column')

    if 'mobility_pred' in speclib._precursor_df.columns:
        df['IonMobility'] = speclib._precursor_df.mobility_pred
    elif 'mobility' in speclib._precursor_df.columns:
        df['IonMobility'] = speclib._precursor_df.mobility

    df['LabelModifiedSequence'] = df['ModifiedPeptide']
    df['StrippedPeptide'] = speclib._precursor_df['sequence']

    if 'precursor_mz' not in speclib._precursor_df.columns:
        speclib.calc_precursor_mz()
    df['PrecursorMz'] = speclib._precursor_df['precursor_mz']

    if 'proteins' in speclib._precursor_df.columns:
        df['ProteinName'] = speclib._precursor_df['proteins']
        df['UniprotID'] = df['ProteinName']
        df['ProteinGroups'] = df['ProteinName']

    if 'uniprot_ids' in speclib._precursor_df.columns:
        df['UniprotID'] = speclib._precursor_df['uniprot_ids']
        if 'ProteinName' not in df.columns:
            df['ProteinName'] = df['UniprotID']
            df['ProteinGroups'] = df['UniprotID']

    if 'genes' in speclib._precursor_df.columns:
        df['Genes'] = speclib._precursor_df['genes']

    if 'protein_group' in speclib._precursor_df.columns:
        df['ProteinGroups'] = speclib._precursor_df['protein_group']

    mask_fragment_intensity_by_mz_(
        speclib._fragment_mz_df,
        speclib._fragment_intensity_df,
        min_frag_mz, max_frag_mz
    )

    df = merge_precursor_fragment_df(
        df,
        speclib._fragment_mz_df,
        speclib._fragment_intensity_df,
        top_n_inten=keep_k_highest_intensity,
        frag_type_head=frag_type_head,
        frag_mass_head=frag_mass_head,
        frag_inten_head=frag_inten_head,
        frag_charge_head=frag_charge_head,
        frag_loss_head=frag_loss_head,
        frag_num_head=frag_num_head,
    )
    df = df[df['RelativeIntensity']>min_frag_intensity]
    df.loc[df[frag_loss_head]=='modloss',frag_loss_head] = modloss

    return df.drop(['frag_start_idx','frag_end_idx'], axis=1)