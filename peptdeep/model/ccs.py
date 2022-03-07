# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/model/ccs.ipynb (unless otherwise specified).

__all__ = ['ModelCCS_Bert', 'ModelCCS_LSTM', 'ccs_to_mobility_pred_df', 'mobility_to_ccs_df_', 'AlphaCCSModel']

# Cell
import torch
import pandas as pd
import numpy as np

from tqdm import tqdm

from alphabase.peptide.fragment import update_precursor_mz

from alphabase.peptide.mobility import (
    ccs_to_mobility_for_df,
    mobility_to_ccs_for_df
)

from peptdeep.model.featurize import (
    parse_aa_indices,
    get_batch_mod_feature
)

from peptdeep.settings import model_const

import peptdeep.model.base as model_base

from peptdeep.model.rt import (
    evaluate_linear_regression,
    evaluate_linear_regression_plot
)

# Cell
class ModelCCS_Bert(torch.nn.Module):
    def __init__(self,
        dropout = 0.1,
        nlayers = 4,
        hidden = 128,
        output_attentions=False,
        **kwargs,
    ):
        super().__init__()

        self.dropout = torch.nn.Dropout(dropout)

        self.input_nn = model_base.AATransformerEncoding(hidden-2)

        self._output_attentions = output_attentions

        self.hidden_nn = model_base.HiddenBert(
            hidden, nlayers=nlayers, dropout=dropout,
            output_attentions=output_attentions
        )

        self.output_nn = torch.nn.Sequential(
            model_base.SeqAttentionSum(hidden),
            torch.nn.PReLU(),
            self.dropout,
            torch.nn.Linear(hidden, 1),
        )

    @property
    def output_attentions(self):
        return self._output_attentions

    @output_attentions.setter
    def output_attentions(self, val:bool):
        self._output_attentions = val
        self.hidden_nn.output_attentions = val

    def forward(self,
        aa_indices,
        mod_x,
        charges:torch.Tensor,
    ):
        x = self.dropout(self.input_nn(
            aa_indices, mod_x
        ))
        charges = charges.unsqueeze(1).repeat(1,x.size(1),2)
        x = torch.cat((x, charges),2)

        hidden_x = self.hidden_nn(x)
        if self.output_attentions:
            self.attentions = hidden_x[1]
        else:
            self.attentions = None
        x = self.dropout(hidden_x[0]+x*0.2)

        return self.output_nn(x).squeeze(1)

# Cell
class ModelCCS_LSTM(torch.nn.Module):
    def __init__(self,
        dropout=0.1,
        *kwargs,
    ):
        super().__init__()

        self.dropout = torch.nn.Dropout(dropout)

        hidden = 256

        self.ccs_encoder = (
            model_base.Input_AA_CNN_LSTM_cat_Charge_Encoder(
                hidden
            )
        )

        self.ccs_decoder = model_base.LinearDecoder(
            hidden+1, 1
        )

    def forward(self,
        aa_indices,
        mod_x,
        charges,
    ):
        x = self.ccs_encoder(aa_indices, mod_x, charges)
        x = self.dropout(x)
        x = torch.cat((x, charges),1)
        return self.ccs_decoder(x).squeeze(1)

# Cell

def ccs_to_mobility_pred_df(
    precursor_df:pd.DataFrame
)->pd.DataFrame:
    """ Add 'mobility_pred' into precursor_df inplace """
    precursor_df[
        'mobility_pred'
    ] = ccs_to_mobility_for_df(
        precursor_df, 'ccs_pred'
    )
    return precursor_df

def mobility_to_ccs_df_(
    precursor_df:pd.DataFrame
)->pd.DataFrame:
    """ Add 'ccs' into precursor_df inplace """
    precursor_df[
        'ccs'
    ] = mobility_to_ccs_for_df(
        precursor_df, 'mobility'
    )
    return precursor_df

# Cell

class AlphaCCSModel(model_base.ModelImplBase):
    def __init__(self,
        dropout=0.1, lr=0.001,
        model_class:torch.nn.Module=ModelCCS_LSTM,
        **kwargs,
    ):
        super().__init__()
        self.build(
            model_class,
            dropout=dropout,
            **kwargs
        )
        self.loss_func = torch.nn.L1Loss()
        self.charge_factor = 0.1

    def _prepare_predict_data_df(self,
        precursor_df:pd.DataFrame,
    ):
        precursor_df['ccs_pred'] = 0.
        self.predict_df = precursor_df

    def _get_features_from_batch_df(self,
        batch_df: pd.DataFrame,
        nAA, **kwargs,
    ):
        aa_indices = torch.LongTensor(
            parse_aa_indices(
                batch_df['sequence'].values.astype('U')
            )
        )

        mod_x_batch = get_batch_mod_feature(batch_df, nAA)
        mod_x = torch.Tensor(mod_x_batch)

        charges = torch.Tensor(
            batch_df['charge'].values
        ).unsqueeze(1)*self.charge_factor

        return aa_indices, mod_x, charges

    def _get_targets_from_batch_df(self,
        batch_df: pd.DataFrame,
        **kwargs,
    ) -> torch.Tensor:
        return torch.Tensor(batch_df['ccs'].values)

    def _set_batch_predict_data(self,
        batch_df: pd.DataFrame,
        predicts,
    ):
        predicts[predicts<0] = 0.0
        if self._predict_in_order:
            self.predict_df.loc[:,'ccs_pred'].values[
                batch_df.index.values[0]:batch_df.index.values[-1]+1
            ] = predicts
        else:
            self.predict_df.loc[
                batch_df.index,'ccs_pred'
            ] = predicts

    def ccs_to_mobility_pred(self,
        precursor_df:pd.DataFrame
    )->pd.DataFrame:
        return ccs_to_mobility_pred_df(precursor_df)