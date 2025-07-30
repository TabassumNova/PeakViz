import pandas as pd
import os
import numpy as np
import hylite
from hylite import io
import copy
import re

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def check_and_extract_line(file_path, search_text):
    with open(file_path, 'r') as file:
        content = file.read()
    if search_text in content:
        # Use regex to find the line starting with the specified 'line' variable
        pattern = f"^{re.escape(search_text)}.*$"
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            return True, match.group(0)
    return False, None

def find_xy(extracted_line):
    if re.search(r'reflectance', extracted_line, re.IGNORECASE):
        return 'wavelength', 'reflectance'
    elif re.search(r'absorbance', extracted_line, re.IGNORECASE):
        wavenumber_present = bool(re.search(r'wavenumber', extracted_line, re.IGNORECASE))
        wavelength_present = bool(re.search(r'nanometer', extracted_line, re.IGNORECASE))
        if wavenumber_present:
            return 'wavenumber', 'absorbance'
        elif wavelength_present:
            return 'wavelength', 'absorbance'


# For point sensors
# Load all type of files
# Reflectance/ Absorbance/ Nanometer/ Wavenumber
def load_data(paths, signal_type, search_text):
    all_energy = []
    ## for reference spectrum
    spectrum_dict = {}
    spectrum_dict['reflectance'] = []
    spectrum_dict['absorbance'] = []
    # if signal_type == 'reference':
    #     refSpectrum_dict = {}
    #     refSpectrum_dict['reflectance'] = []
    #     refSpectrum_dict['absorbance'] = []

    ###
    for file_path in paths:
        seach_text_present, extracted_line = check_and_extract_line(file_path, search_text)
        x_axis, y_axis = find_xy(extracted_line)
        if y_axis != signal_type and signal_type != 'reference':
            return None, None

        filename = os.path.basename(file_path)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if x_axis == 'wavelength':
            sample_energy = [filename]
            wavelength_list = ['sample']
            for line0 in lines:
                line = line0.strip().split(" ")
                if is_float(line[0]):
                    wavelength = float(line[0])
                    energy = float(line[-1])
                    sample_energy.append(energy)
                    wavelength_list.append(wavelength)
            # all_energy.append(sample_energy)
            spectrum_dict[y_axis].append(sample_energy)

        elif x_axis == 'wavenumber':
            sample_energy = []
            wavelength_list = []
            for line0 in lines:
                line = line0.strip().split(" ")
                if is_float(line[0]):
                    energy = float(line[-1])
                    sample_energy = [energy] + sample_energy
                    # TODO
                    # Fill wavelength list only for one sample file to avoid
                    # iterative process
                    wavenumber = float(line[0])
                    wavelength = (1/wavenumber)* (10 ** 7)
                    wavelength_list = [wavelength] + wavelength_list
            wavelength_list = ['sample'] + wavelength_list
            sample_energy = [filename] + sample_energy
            # all_energy.append(sample_energy)
            spectrum_dict[y_axis].append(sample_energy)

    if len(spectrum_dict['reflectance']) == 0:
        reflectance_df = None
    else:
        reflectance_df = pd.DataFrame(spectrum_dict['reflectance'], columns=wavelength_list)
    if len(spectrum_dict['absorbance']) == 0:
        absorbance_df = None
    else:
        absorbance_df = pd.DataFrame(spectrum_dict['absorbance'], columns=wavelength_list)
    
    return reflectance_df, absorbance_df
    # df = pd.DataFrame(spectrum_dict, columns=wavelength_list)
    # return df


def load_refSpectrum(spectrum_paths):
    all_energy = []
    for file_path in spectrum_paths:
        filename = os.path.basename(file_path)
        sample_energy = []
        wavelength_list = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line0 in lines:
            line = line0.strip().split(" ")
            if is_float(line[1]):
                wavelength = float(line[1])
                energy = float(line[-1])
                sample_energy.append(energy)
                wavelength_list.append(wavelength)
                pass
        wavelength_list = ['polymer'] + wavelength_list
        sample_energy = [filename] + sample_energy
        all_energy.append(sample_energy)
    refSpectrum_df = pd.DataFrame(all_energy, columns=wavelength_list)
    return refSpectrum_df

# For Image sensor
def create_masked_spec(folder_path):
    # create 'masked_spetrum' folder
    output_path = os.path.join(folder_path, 'masked_spectrum')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Folder '{output_path}' created successfully.")
    else:
        print(f"Folder '{output_path}' already exists.")

    # Load all the sensor data
    mask_path = os.path.join(folder_path, 'mask.hdr')
    fenix_path = os.path.join(folder_path, 'FENIX.hdr')
    fx50_path = os.path.join(folder_path, 'FX50.hdr')
    lwir_path = os.path.join(folder_path, 'LWIR.hdr')
    mask = io.load(mask_path)
    fenix = io.load(fenix_path)
    fx50 = io.load(fx50_path)
    lwir = io.load(lwir_path)

    fenix.data = fenix.data/float(io.loadHeader(fenix_path)['reflectance scale factor'])
    fx50.data = fx50.data/float(io.loadHeader(fx50_path)['reflectance scale factor'])
    lwir.data = lwir.data/float(io.loadHeader(lwir_path)['reflectance scale factor'])

    sensors = {'FENIX':fenix,
               'FX50':fx50,
               'LWIR':lwir,}
    mask_labels = np.unique(mask.data)

    # Collect decoder file
    decoder_path = os.path.join(folder_path, 'decoder.xlsx')
    if os.path.exists(decoder_path):
        decoder_df = pd.read_excel(decoder_path)
    else:
        decoder_df = None
        sample_name = ''

    final_df = None
    for s_key, s_value in sensors.items():
        wavelengths = [float(w) for w in s_value.get_wavelengths()]
        s_value.data = s_value.data[0:mask.data.shape[0], 0:mask.data.shape[1], :]
        s_value[:,:,:][mask[:,:,0]==0] = np.nan
        sample_list = []
        for label in mask_labels:
            if label:
                if decoder_df is not None:
                    sample_name = decoder_df[decoder_df['mask']==label]['name'].values[0]
                else:
                    sample_name = 'mask_'+str(label)
                sensor_path = os.path.join(output_path, s_key)
                if not os.path.exists(sensor_path):
                    os.makedirs(sensor_path)
                spectrum_path = os.path.join(sensor_path, (sample_name + '_' + s_key + '.hdr'))
                # if the path not exist then create header file
                # otherwise just load the file
                if not os.path.exists(spectrum_path):
                    sample = copy.deepcopy(s_value)
                    sample[:,:,:][mask[:,:,0]!=label] = np.nan
                    sample.data = sample.data.reshape(-1,sample.data.shape[-1])
                    sample_spec = sample.data[~np.isnan(sample.data).all(axis=1)]
                    # Save non_nan_values as sample_sensor.lib in a folder
                    lib = hylite.HyLibrary(sample_spec, wav=s_value.get_wavelengths())
                    io.save(spectrum_path, lib)
                else:
                    lib = io.load(spectrum_path)
                    sample_spec = np.squeeze(lib.data, axis=1)
                # For averaged_data plotting 
                averaged_data = [sample_name] + np.mean(sample_spec, axis=0, keepdims=True).tolist()[0]
                sample_list.append(averaged_data)
        df = pd.DataFrame(sample_list, columns=['sample']+ wavelengths)
        if final_df is None:
            final_df = df
        else:
            final_df = pd.merge(final_df, df, on='sample', how='outer')

    return final_df

# For Image sensor
# For loading saved hylib object
# Select sample objects from only one sensor
# Check if those are from the same sensor
# otherwise through error
def load_hylib(header_files):
    hylib_dict = {}
    wavelengths = None
    for file in header_files:
        _, name = os.path.split(file)
        header = io.load(file)
        if wavelengths is not None:
            check = np.array_equal(wavelengths, header.get_wavelengths())
            if check==False:
                return None
        wavelengths = header.get_wavelengths()
        data = np.squeeze(header.data, axis=1)
        df = pd.DataFrame(data, columns=header.get_wavelengths())
        hylib_dict[name] = df
    return hylib_dict








    