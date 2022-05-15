# AUTOGENERATED BY NBDEV! DO NOT EDIT!

__all__ = ["index", "modules", "custom_doc_links", "git_url"]

index = {"match_centroid_mz": "match.ipynb",
         "match_one_raw_with_numba": "match.ipynb",
         "PepSpecMatch": "match.ipynb",
         "MSReaderBase": "ms_reader.ipynb",
         "AlphaPept_HDF_MS1_Reader": "ms_reader.ipynb",
         "AlphaPept_HDF_MS2_Reader": "ms_reader.ipynb",
         "read_until": "ms_reader.ipynb",
         "find_line": "ms_reader.ipynb",
         "parse_pfind_scan_from_TITLE": "ms_reader.ipynb",
         "is_pfind_mgf": "ms_reader.ipynb",
         "index_ragged_list": "ms_reader.ipynb",
         "MGFReader": "ms_reader.ipynb",
         "MSReaderProvider": "ms_reader.ipynb",
         "ms2_reader_provider": "ms_reader.ipynb",
         "ms1_reader_provider": "ms_reader.ipynb",
         "mod_feature_size": "rt.ipynb",
         "max_instrument_num": "ms2.ipynb",
         "frag_types": "ms2.ipynb",
         "max_frag_charge": "ms2.ipynb",
         "num_ion_types": "ms2.ipynb",
         "aa_embedding_size": "building_block.ipynb",
         "aa_embedding": "building_block.ipynb",
         "ascii_embedding": "building_block.ipynb",
         "aa_one_hot": "building_block.ipynb",
         "instrument_embedding": "building_block.ipynb",
         "zero_param": "building_block.ipynb",
         "xavier_param": "building_block.ipynb",
         "init_state": "building_block.ipynb",
         "SeqCNN_MultiKernel": "building_block.ipynb",
         "SeqCNN": "building_block.ipynb",
         "Seq_Transformer": "building_block.ipynb",
         "Hidden_Transformer": "building_block.ipynb",
         "Hidden_HFace_Transformer": "building_block.ipynb",
         "HiddenBert": "building_block.ipynb",
         "SeqLSTM": "building_block.ipynb",
         "SeqGRU": "building_block.ipynb",
         "SeqAttentionSum": "building_block.ipynb",
         "PositionalEncoding": "building_block.ipynb",
         "PositionalEmbedding": "building_block.ipynb",
         "AA_Mod_Embedding": "building_block.ipynb",
         "Meta_Embedding": "building_block.ipynb",
         "Mod_Embedding_FixFirstK": "building_block.ipynb",
         "Mod_Embedding": "building_block.ipynb",
         "Input_AA_Mod_PositionalEncoding": "building_block.ipynb",
         "Input_AA_Mod_Charge_PositionalEncoding": "building_block.ipynb",
         "InputAAEmbedding": "building_block.ipynb",
         "InputMetaNet": "building_block.ipynb",
         "InputModNetFixFirstK": "building_block.ipynb",
         "InputModNet": "building_block.ipynb",
         "AATransformerEncoding": "building_block.ipynb",
         "Input_AA_Mod_LSTM": "building_block.ipynb",
         "Input_AA_Mod_Meta_LSTM": "building_block.ipynb",
         "Input_AA_Mod_Charge_LSTM": "building_block.ipynb",
         "InputAALSTM": "building_block.ipynb",
         "InputAALSTM_cat_Meta": "building_block.ipynb",
         "InputAALSTM_cat_Charge": "building_block.ipynb",
         "Seq_Meta_LSTM": "building_block.ipynb",
         "Seq_Meta_Linear": "building_block.ipynb",
         "OutputLSTM_cat_Meta": "building_block.ipynb",
         "OutputLinear_cat_Meta": "building_block.ipynb",
         "Encoder_AA_Mod_LSTM": "building_block.ipynb",
         "Encoder_AA_Mod_CNN_LSTM": "building_block.ipynb",
         "Encoder_AA_Mod_CNN_LSTM_AttnSum": "building_block.ipynb",
         "Encoder_AA_Mod_Transformer": "building_block.ipynb",
         "Encoder_AA_Mod_Transformer_AttnSum": "building_block.ipynb",
         "Encoder_AA_Mod_Charge_Transformer": "building_block.ipynb",
         "Encoder_AA_Mod_Charge_Transformer_AttnSum": "building_block.ipynb",
         "Encoder_AA_Mod_Charge_CNN_LSTM_AttnSum": "building_block.ipynb",
         "Encoder_HFace_Transformer": "building_block.ipynb",
         "Input_AA_LSTM_Encoder": "building_block.ipynb",
         "Input_AA_CNN_Encoder": "building_block.ipynb",
         "Input_AA_CNN_LSTM_Encoder": "building_block.ipynb",
         "Input_AA_CNN_LSTM_cat_Charge_Encoder": "building_block.ipynb",
         "Decoder_LSTM": "building_block.ipynb",
         "Decoder_GRU": "building_block.ipynb",
         "SeqLSTMDecoder": "building_block.ipynb",
         "SeqGRUDecoder": "building_block.ipynb",
         "Decoder_Linear": "building_block.ipynb",
         "LinearDecoder": "building_block.ipynb",
         "Model_CCS_Bert": "ccs.ipynb",
         "Model_CCS_LSTM": "ccs.ipynb",
         "ccs_to_mobility_pred_df": "ccs.ipynb",
         "mobility_to_ccs_df_": "ccs.ipynb",
         "AlphaCCSModel": "ccs.ipynb",
         "get_all_mod_features": "featurize.ipynb",
         "mod_elements": "featurize.ipynb",
         "mod_elem_to_idx": "featurize.ipynb",
         "MOD_TO_FEATURE": "featurize.ipynb",
         "parse_mod_feature": "featurize.ipynb",
         "get_batch_mod_feature": "featurize.ipynb",
         "get_batch_aa_indices": "featurize.ipynb",
         "get_ascii_indices": "featurize.ipynb",
         "instrument_dict": "featurize.ipynb",
         "unknown_inst_index": "featurize.ipynb",
         "parse_instrument_indices": "featurize.ipynb",
         "get_cosine_schedule_with_warmup": "model_interface.ipynb",
         "append_nAA_column_if_missing": "model_interface.ipynb",
         "ModelInterface": "model_interface.ipynb",
         "ModelMS2Transformer": "ms2.ipynb",
         "ModelMS2Bert": "ms2.ipynb",
         "ModelMS2pDeep": "ms2.ipynb",
         "IntenAwareLoss": "ms2.ipynb",
         "pDeepModel": "ms2.ipynb",
         "normalize_training_intensities": "ms2.ipynb",
         "pearson_correlation": "ms2.ipynb",
         "spectral_angle": "ms2.ipynb",
         "spearman_correlation": "ms2.ipynb",
         "add_cutoff_metric": "ms2.ipynb",
         "calc_ms2_similarity": "ms2.ipynb",
         "pearson": "ms2.ipynb",
         "spearman": "ms2.ipynb",
         "IRT_PEPTIDE_DF": "rt.ipynb",
         "irt_pep": "rt.ipynb",
         "Model_RT_Bert": "rt.ipynb",
         "Model_RT_LSTM_CNN": "rt.ipynb",
         "Model_RT_LSTM": "rt.ipynb",
         "AlphaRTModel": "rt.ipynb",
         "is_model_zip": "pretrained_models.ipynb",
         "download_models": "pretrained_models.ipynb",
         "install_models": "pretrained_models.ipynb",
         "sandbox_dir": "pretrained_models.ipynb",
         "model_name": "pretrained_models.ipynb",
         "model_url": "pretrained_models.ipynb",
         "url_zip_name": "pretrained_models.ipynb",
         "model_zip": "pretrained_models.ipynb",
         "count_mods": "pretrained_models.ipynb",
         "psm_sampling_with_important_mods": "pretrained_models.ipynb",
         "load_phos_models": "pretrained_models.ipynb",
         "load_models": "pretrained_models.ipynb",
         "load_models_by_model_type_in_zip": "pretrained_models.ipynb",
         "mgr_settings": "pretrained_models.ipynb",
         "clear_error_modloss_intensities": "pretrained_models.ipynb",
         "ModelManager": "pretrained_models.ipynb",
         "protease_dict": "fasta.ipynb",
         "read_fasta_file": "fasta.ipynb",
         "load_all_proteins": "fasta.ipynb",
         "concat_proteins": "fasta.ipynb",
         "cleave_sequence_with_cut_pos": "fasta.ipynb",
         "Digest": "fasta.ipynb",
         "get_fix_mods": "fasta.ipynb",
         "get_candidate_sites": "fasta.ipynb",
         "get_var_mod_sites": "fasta.ipynb",
         "get_var_mods_per_sites_multi_mods_on_aa": "fasta.ipynb",
         "get_var_mods_per_sites_single_mod_on_aa": "fasta.ipynb",
         "get_var_mods": "fasta.ipynb",
         "get_var_mods_per_sites": "fasta.ipynb",
         "parse_term_mod": "fasta.ipynb",
         "add_single_peptide_labeling": "fasta.ipynb",
         "parse_labels": "fasta.ipynb",
         "create_labeling_peptide_df": "fasta.ipynb",
         "protein_idxes_to_names": "fasta.ipynb",
         "PredictFastaSpecLib": "fasta.ipynb",
         "append_regular_modifications": "fasta.ipynb",
         "get_lcp_array": "lcp_digest.ipynb",
         "get_next_stop_char": "lcp_digest.ipynb",
         "get_all_substring_indices_from_lcp": "lcp_digest.ipynb",
         "get_substring_indices": "lcp_digest.ipynb",
         "SpectronautMSMSReader": "library_frag_reader.ipynb",
         "keep_high_prob_phos": "maxquant_frag_reader.ipynb",
         "filter_phos": "maxquant_frag_reader.ipynb",
         "MaxQuantMSMSReader": "maxquant_frag_reader.ipynb",
         "PSMReader_w_FragBase": "psm_frag_reader.ipynb",
         "PSM_w_FragReaderProvider": "psm_frag_reader.ipynb",
         "psm_w_frag_reader_provider": "psm_frag_reader.ipynb",
         "PSMLabelReader": "psmlabel_reader.ipynb",
         "load_psmlabel_list": "psmlabel_reader.ipynb",
         "fdr_to_q_values": "fdr.ipynb",
         "calc_fdr": "fdr.ipynb",
         "fdr_from_ref": "fdr.ipynb",
         "calc_fdr_from_ref": "fdr.ipynb",
         "calc_fdr_for_df": "fdr.ipynb",
         "calc_fdr_from_ref_for_df": "fdr.ipynb",
         "match_one_raw": "feature_extractor.ipynb",
         "get_ms2_features": "feature_extractor.ipynb",
         "match_one_raw_mp": "feature_extractor.ipynb",
         "get_ms2_features_mp": "feature_extractor.ipynb",
         "perc_settings": "percolator.ipynb",
         "ScoreFeatureExtractor": "feature_extractor.ipynb",
         "ScoreFeatureExtractorMP": "feature_extractor.ipynb",
         "LogisticRegressionTorch": "percolator.ipynb",
         "RescoreModelProvider": "percolator.ipynb",
         "NNRescore": "percolator.ipynb",
         "rescore_model_provider": "percolator.ipynb",
         "Percolator": "percolator.ipynb",
         "update_settings": "settings.ipynb",
         "update_modifications": "settings.ipynb",
         "global_settings": "settings.ipynb",
         "model_const": "settings.ipynb",
         "PredictLibraryMakerBase": "library_factory.ipynb",
         "PrecursorLibraryMaker": "library_factory.ipynb",
         "PeptideLibraryMaker": "library_factory.ipynb",
         "SequenceLibraryMaker": "library_factory.ipynb",
         "FastaLibraryMaker": "library_factory.ipynb",
         "LibraryMakerProvider": "library_factory.ipynb",
         "library_maker_provider": "library_factory.ipynb",
         "PredictSpecLib": "predict_lib.ipynb",
         "lib_settings": "predict_lib.ipynb",
         "create_modified_sequence": "translate.ipynb",
         "merge_precursor_fragment_df": "translate.ipynb",
         "is_nterm_frag": "translate.ipynb",
         "mask_fragment_intensity_by_mz_": "translate.ipynb",
         "mask_fragment_intensity_by_frag_nAA": "translate.ipynb",
         "speclib_to_single_df": "translate.ipynb",
         "speclib_to_swath_df": "translate.ipynb",
         "translate_to_tsv": "translate.ipynb",
         "mod_to_other_mod_dict": "translate.ipynb",
         "mod_to_unimod_dict": "translate.ipynb",
         "process_bar": "utils.ipynb",
         "set_logger": "utils.ipynb",
         "show_platform_info": "utils.ipynb",
         "show_python_info": "utils.ipynb",
         "BASE_PATH": "utils.ipynb",
         "LOG_PATH": "utils.ipynb",
         "explode_multiple_columns": "utils.ipynb",
         "regional_sampling": "utils.ipynb",
         "uniform_sampling": "utils.ipynb",
         "evaluate_linear_regression": "utils.ipynb",
         "evaluate_linear_regression_plot": "utils.ipynb"}

modules = ["mass_spec/match.py",
           "mass_spec/ms_reader.py",
           "model/building_block.py",
           "model/ccs.py",
           "model/featurize.py",
           "model/model_interface.py",
           "model/ms2.py",
           "model/rt.py",
           "pretrained_models.py",
           "protein/fasta.py",
           "protein/inference.py",
           "protein/lcp_digest.py",
           "psm_frag_reader/library_frag_reader.py",
           "psm_frag_reader/maxquant_frag_reader.py",
           "psm_frag_reader/psm_frag_reader.py",
           "psm_frag_reader/psmlabel_reader.py",
           "rescore/fdr.py",
           "rescore/feature_extractor.py",
           "rescore/percolator.py",
           "settings.py",
           "spec_lib/library_factory.py",
           "spec_lib/predict_lib.py",
           "spec_lib/translate.py",
           "utils.py"]

doc_url = "https://MannLabs.github.io/peptdeep/"

git_url = "https://github.com/MannLabs/peptdeep/tree/main/"

def custom_doc_links(name): return None
