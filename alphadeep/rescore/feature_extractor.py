# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/rescore/feature_extractor.ipynb (unless otherwise specified).

__all__ = ['ScoreFeatureExtractor', 'ScoreFeatureExtractor_wo_MS2']

# Cell
import pandas as pd
import numpy as np

from alphadeep.pretrained_models import ModelManager
from alphadeep.model.ms2 import calc_ms2_similarity
from alphadeep.mass_spec.match import PepSpecMatch
from alphabase.peptide.fragment import get_charged_frag_types

class ScoreFeatureExtractor(object):
    def __init__(self, model_mgr=None):
        if model_mgr is None:
            self.model_mgr = ModelManager()
            self.model_mgr.load_installed_models()
        else:
            self.model_mgr = model_mgr

        self.model_fine_tuning = True

        self.score_feature_list = [
            'cos','sa','spc',
            'cos_bion','sa_bion','spc_bion',
            'cos_yion','sa_yion','spc_yion',
            'frag_ratio','frag_ratio_bion',
            'frag_ratio_yion','rt_delta_abs',
            'mobility_delta_abs',
        ]

    def extract_rt_features(self):
        if 'rt_norm' in self.psm_df.columns:
            if self.psm_tune_df is not None:
                self.model_mgr.fine_tune_rt_model(self.psm_tune_df)

            self.psm_df = self.model_mgr.rt_model.predict(
                self.psm_df
            )

            self.psm_df[
                'rt_delta'
            ] = (
                self.psm_df.rt_pred-self.psm_df.rt_norm
            )

            self.psm_df[
                'rt_delta_abs'
            ] = self.psm_df.rt_delta.abs()
        else:
            self.psm_df['rt_delta'] = 0
            self.psm_df['rt_delta_abs'] = 0

    def extract_mobility_features(self):
        if (
            'mobility' in self.psm_df.columns
        ):
            if self.psm_tune_df is not None:
                self.model_mgr.fine_tune_ccs_model(self.psm_tune_df)

            self.psm_df = self.model_mgr.ccs_model.predict(
                self.psm_df
            )

            self.psm_df = self.ccs_model.ccs_to_mobility_pred(
                self.psm_df
            )

            self.psm_df[
                'mobility_delta'
            ] = (
                self.psm_df.mobility_pred-self.psm_df.mobility
            )
            self.psm_df[
                self.psm_df.mobility_delta.isna(),'mobility_delta'
            ] = 0
            self.psm_df['mobility_delta_abs'] = self.psm_df.mobility_delta.abs()
        else:
            self.psm_df['mobility_delta'] = 0
            self.psm_df['mobility_delta_abs'] = 0

    def _get_tuning_psm_df(self):
        if self.model_fine_tuning:
            self.psm_tune_df = self.psm_df[
                (self.psm_df.fdr<0.01)
                &(self.psm_df.decoy==0)
            ].sample(
                self.model_mgr.n_psm_to_tune_ms2
            ).copy()
        else:
            self.psm_tune_df = None

    def extract_features(self,
        psm_df: pd.DataFrame,
        ms2_file_dict, #raw_name: ms2_file_path or ms_reader object
        ms2_file_type:str = 'alphapept', #or 'mgf', or 'thermo'
        frag_types_to_match:list = get_charged_frag_types(['b','y'], 2),
        ms2_ppm=True, ms2_tol=20,
    )->pd.DataFrame:
        self.match = PepSpecMatch(psm_df,
            charged_frag_types=frag_types_to_match
        )

        self.match.match_ms2_centroid(
            ms2_file_dict=ms2_file_dict,
            ms2_file_type=ms2_file_type,
            ppm=ms2_ppm, tol=ms2_tol,
        )

        self.psm_df = self.match.psm_df

        self._get_tuning_psm_df()

        self.extract_rt_features()
        self.extract_mobility_features()


        self.matched_mz_err_df = self.match.matched_mz_err_df
        self.matched_intensity_df = self.match.matched_intensity_df

        if self.psm_tune_df is not None:
            self.model_mgr.fine_tune_ms2_model(
                self.psm_tune_df, self.matched_intensity_df
            )

        if 'nce' not in self.psm_df.columns:
            self.psm_df['nce'] = self.model_mgr.nce
            self.psm_df['instrument'] = self.model_mgr.instrument

        self.predict_intensity_df = self.model_mgr.ms2_model.predict(
            self.psm_df, reference_frag_df=self.matched_intensity_df
        )
        used_frag_types = []
        for frag_type in frag_types_to_match:
            if frag_type in self.model_mgr.ms2_model.charged_frag_types:
                used_frag_types.append(frag_type)
        self.predict_intensity_df = self.predict_intensity_df[
            used_frag_types
        ]

        self.psm_df, ms2_metrics_df = calc_ms2_similarity(
            self.psm_df, self.predict_intensity_df,
            self.matched_intensity_df,
            charged_frag_types=used_frag_types,
            metrics=['COS','SA','SPC'],
        )
        self.psm_df.rename(
            columns={
                'COS':'cos','SA':'sa','SPC':'spc'
            },
            inplace=True
        )

        b_frag_types = [
            _t for _t in used_frag_types
            if _t.startswith('b')
        ]
        y_frag_types = [
            _t for _t in used_frag_types
            if _t.startswith('y')
        ]

        frag_position_hits = self.matched_intensity_df[
            used_frag_types
        ].values.any(axis=1)
        frag_ratio_ion = []
        for start_idx, end_idx in self.psm_df[
            ['frag_start_idx','frag_end_idx']
        ].values:
            frag_ratio_ion.append(
                np.mean(frag_position_hits[start_idx:end_idx])
            )
        self.psm_df['frag_ratio'] = frag_ratio_ion

        if len(b_frag_types) > 0:
            self.psm_df, ms2_metrics_df = calc_ms2_similarity(
                self.psm_df, self.predict_intensity_df,
                self.matched_intensity_df,
                charged_frag_types=b_frag_types,
                metrics=['COS','SA','SPC'],
            )
            self.psm_df.rename(
                columns={
                    'COS':'cos_bion','SA':'sa_bion','SPC':'spc_bion'
                },
                inplace=True
            )
            frag_position_hits = self.matched_intensity_df[
                b_frag_types
            ].values.any(axis=1)
            frag_ratio_ion = []
            for start_idx, end_idx in self.psm_df[
                ['frag_start_idx','frag_end_idx']
            ].values:
                frag_ratio_ion.append(
                    np.mean(frag_position_hits[start_idx:end_idx])
                )
            self.psm_df['frag_ratio_bion'] = frag_ratio_ion
        else:
            self.psm_df[['cos_bion','sa_bion','spc_bion']] = 0
            self.psm_df[['frag_ratio_bion']] = 0

        if len(y_frag_types) > 0:
            self.psm_df, ms2_metrics_df = calc_ms2_similarity(
                self.psm_df, self.predict_intensity_df,
                self.matched_intensity_df,
                charged_frag_types=y_frag_types,
                metrics=['COS','SA','SPC'],
            )
            self.psm_df.rename(
                columns={
                    'COS':'cos_yion','SA':'sa_yion','SPC':'spc_yion'
                },
                inplace=True
            )
            frag_position_hits = self.matched_intensity_df[
                y_frag_types
            ].values.any(axis=1)
            frag_ratio_ion = []
            for start_idx, end_idx in self.psm_df[
                ['frag_start_idx','frag_end_idx']
            ].values:
                frag_ratio_ion.append(
                    np.mean(frag_position_hits[start_idx:end_idx])
                )
            self.psm_df['frag_ratio_yion'] = frag_ratio_ion
        else:
            self.psm_df[['cos_yion','sa_yion','spc_yion']] = 0
            self.psm_df[['frag_ratio_yion']] = 0

        return self.psm_df


# Cell
class ScoreFeatureExtractor_wo_MS2(ScoreFeatureExtractor):
    def __init__(self, model_mgr=None):
        super().__init__(model_mgr=model_mgr)

        self.score_feature_list = [
            'rt_delta_abs',
            'mobility_delta_abs',
        ]
    def extract_features(self,
        psm_df: pd.DataFrame,
        *args,
        **kwargs
    ) -> pd.DataFrame:
        self.psm_df = psm_df

        self._get_tuning_psm_df()

        self.extract_rt_features()
        self.extract_mobility_features()

        return self.psm_df