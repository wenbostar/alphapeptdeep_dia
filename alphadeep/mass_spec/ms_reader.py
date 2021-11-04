# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/mass_spec/ms_reader.ipynb (unless otherwise specified).

__all__ = ['MSReaderBase', 'AlphaPept_HDF_MS1_Reader', 'AlphaPept_HDF_MS2_Reader', 'read_until', 'find_line',
           'parse_pfind_scan_from_TITLE', 'is_pfind_mgf', 'index_ragged_list', 'MGFReader', 'MSReaderProvider',
           'ms2_reader_provider', 'ms1_reader_provider']

# Cell
import os
import numpy as np
import pandas as pd

class MSReaderBase:
    def __init__(self):
        self.spectrum_df:pd.DataFrame = None
        self.masses: np.array = None
        self.intens: np.array = None

    def load(self, file_path):
        raise NotImplementedError('load()')

    def build_spectrum_df(self, scan_list, scan_indices, rt_list, mobility_list = None):
        if not mobility_list: mobility_list = np.nan
        self.spectrum_df = pd.DataFrame({
            'scan_no': scan_list,
            'peak_start_idx': scan_indices[:-1],
            'peak_end_idx': scan_indices[1:],
            'RT': rt_list,
            'mobility': mobility_list,
        }, index = scan_list)

    def get_peaks(self, scan_no):
        if scan_no not in self.spectrum_df.index:
            return None, None
        start_idx, end_idx = self.spectrum_df.loc[
            scan_no, ['peak_start_idx','peak_end_idx']
        ].values.astype(np.int64)
        return (
            self.masses[start_idx:end_idx],
            self.intens[start_idx:end_idx]
        )

class AlphaPept_HDF_MS1_Reader(MSReaderBase):
    def load(self, file_path):
        from alphapept.io import HDF_File
        hdf_file = HDF_File(file_path)
        self.ms_data = {}
        for dataset_name in hdf_file.read(group_name="Raw/MS1_scans"):
            values = hdf_file.read(
                dataset_name=dataset_name,
                group_name="Raw/MS1_scans",
            )
            self.ms_data[dataset_name] = values
        self.masses = self.ms_data['mass_list_ms1']
        self.intens = self.ms_data['int_list_ms1']
        self.build_spectrum_df(
            scan_list=self.ms_data['scan_list_ms1'],
            scan_indices=self.ms_data['indices_ms1'],
            rt_list=self.ms_dat['rt_list_ms1'],
            mobility_list=self.ms_data['mobility'] if 'mobility' in self.ms_data else None,
        )

class AlphaPept_HDF_MS2_Reader(MSReaderBase):
    def load(self, file_path):
        from alphapept.io import HDF_File
        hdf_file = HDF_File(file_path)
        self.ms_data = {}
        for dataset_name in hdf_file.read(group_name="Raw/MS2_scans"):
            values = hdf_file.read(
                dataset_name=dataset_name,
                group_name="Raw/MS2_scans",
            )
            self.ms_data[dataset_name] = values
        self.masses = self.ms_data['mass_list_ms2']
        self.intens = self.ms_data['int_list_ms2']
        self.build_spectrum_df(
            scan_list=self.ms_data['scan_list_ms2'],
            scan_indices=self.ms_data['indices_ms2'],
            rt_list=self.ms_dat['rt_list_ms2'],
            mobility_list=self.ms_data['mobility2'] if 'mobility2' in self.ms_data else None,
        )

def read_until(file, until):
    lines = []
    while True:
        line = file.readline().strip()
        if line.startswith(until):
            break
        else:
            lines.append(line)
    return lines

def find_line(lines, start):
    for line in lines:
        if line.startswith(start):
            return line
    return None

def parse_pfind_scan_from_TITLE(pfind_title):
    return int(pfind_title.split('.')[-4])

def is_pfind_mgf(mgf):
    return mgf.upper().endswith('_HCDFT.MGF')

def index_ragged_list(ragged_list: list)  -> np.ndarray:
    """Create lookup indices for a list of arrays for concatenation.

    Args:
        value (list): Input list of arrays.

    Returns:
        indices: A numpy array with indices.
    """
    indices = np.zeros(len(ragged_list) + 1, np.int64)
    indices[1:] = [len(i) for i in ragged_list]
    indices = np.cumsum(indices)

    return indices

class MGFReader(MSReaderBase):

    def load(self, mgf):
        if isinstance(mgf, str):
            f = open(mgf)
        else:
            f = mgf
        scanset = set()
        masses_list = []
        intens_list = []
        scan_list = []
        rt_list = []
        while True:
            line = f.readline()
            if not line: break
            if line.startswith('BEGIN IONS'):
                lines = read_until(f, 'END IONS')
                masses = []
                intens = []
                scan = None
                RT = 0
                for line in lines:
                    if line[0].isdigit():
                        mass,inten = [float(i) for i in line.strip().split()]
                        masses.append(mass)
                        intens.append(inten)
                    elif line.startswith('SCAN='):
                        scan = int(line.split('=')[1])
                    elif line.startswith('RTINSECOND'):
                        RT = float(line.split('=')[1])
                if not scan:
                    title = find_line(lines, 'TITLE=')
                    scan = parse_pfind_scan_from_TITLE(title)
                if scan in scanset: continue
                scanset.add(scan)
                scan_list.append(scan)
                rt_list.append(RT)
                masses_list.append(np.array(masses))
                intens_list.append(np.array(intens))
        if isinstance(mgf, str):
            f.close()
        self.build_spectrum_df(
            scan_list,
            index_ragged_list(masses_list),
            rt_list
        )
        self.masses = np.concatenate(masses_list)
        self.intens = np.concatenate(intens_list)


class MSReaderProvider:
    def __init__(self):
        self.reader_dict = {}
    def register_reader(self, ms2_type, reader_class):
        self.reader_dict[ms2_type.lower()] = reader_class

    def get_reader(self, file_type)->MSReaderBase:
        if file_type not in self.reader_dict: return None
        else: return self.reader_dict[file_type.lower()]()

ms2_reader_provider = MSReaderProvider()
ms2_reader_provider.register_reader('mgf', MGFReader)
ms2_reader_provider.register_reader('alphapept', AlphaPept_HDF_MS2_Reader)
ms2_reader_provider.register_reader('alphapept_hdf', AlphaPept_HDF_MS2_Reader)

ms1_reader_provider = MSReaderProvider()
ms1_reader_provider.register_reader('alphapept', AlphaPept_HDF_MS1_Reader)
ms1_reader_provider.register_reader('alphapept_hdf', AlphaPept_HDF_MS1_Reader)

# Cell

try:
    from alphapept.pyrawfilereader import RawFileReader
    class ThermoRawMS1Reader(MSReaderBase):
        def __init__(self):
            super().__init__()
            self.profile_mode = False

        def load(self, raw_path):
            rawfile = RawFileReader(raw_path)

            spec_indices = np.array(
                range(rawfile.FirstSpectrumNumber, rawfile.LastSpectrumNumber + 1)
            )
            scan_list = []
            rt_list = []
            masses_list = []
            intens_list = []
            for i in spec_indices:
                try:
                    ms_order = rawfile.GetMSOrderForScanNum(i)

                    if ms_order == 1:
                        if self.profile_mode:
                            masses, intens = rawfile.GetProfileMassListFromScanNum(i)
                        else:
                            masses, intens = rawfile.GetCentroidMassListFromScanNum(i)
                        scan_list.append(i)
                        rt_list.append(rawfile.RTInSecondsFromScanNum(i))
                        masses_list.append(masses)
                        intens_list.append(intens)

                except KeyboardInterrupt as e:
                    raise e
                except SystemExit as e:
                    raise e
                except Exception as e:
                    print(f"Bad scan={i} in raw file '{raw_path}'")

            self.build_spectrum_df(
                scan_list,
                index_ragged_list(masses_list),
                rt_list,
            )
            self.masses = np.concatenate(masses_list)
            self.intens = np.concatenate(intens_list)
            rawfile.Close()

    class ThermoRawMS2Reader(MSReaderBase):
        def __init__(self):
            super().__init__()
            self.profile_mode = False

        def load(self, raw_path):
            rawfile = RawFileReader(raw_path)

            spec_indices = np.array(
                range(rawfile.FirstSpectrumNumber, rawfile.LastSpectrumNumber + 1)
            )
            scan_list = []
            rt_list = []
            masses_list = []
            intens_list = []
            for i in spec_indices:
                try:
                    ms_order = rawfile.GetMSOrderForScanNum(i)

                    if ms_order == 2:
                        if self.profile_mode:
                            masses, intens = rawfile.GetProfileMassListFromScanNum(i)
                        else:
                            masses, intens = rawfile.GetCentroidMassListFromScanNum(i)
                        scan_list.append(i)
                        rt_list.append(rawfile.RTInSecondsFromScanNum(i))
                        masses_list.append(masses)
                        intens_list.append(intens)

                except KeyboardInterrupt as e:
                    raise e
                except SystemExit as e:
                    raise e
                # except Exception as e:
                #     print(f"Bad scan={i} in raw file '{raw_path}'")

            self.build_spectrum_df(
                scan_list,
                index_ragged_list(masses_list),
                rt_list,
            )
            self.masses = np.concatenate(masses_list)
            self.intens = np.concatenate(intens_list)
            rawfile.Close()

    ms2_reader_provider.register_reader('thermo', ThermoRawMS2Reader)
    ms2_reader_provider.register_reader('thermo_raw', ThermoRawMS2Reader)
    ms1_reader_provider.register_reader('thermo', ThermoRawMS1Reader)
    ms1_reader_provider.register_reader('thermo_raw', ThermoRawMS1Reader)
except Exception as e:
    # alphapept or RawFileReader is not installed
    print(e)