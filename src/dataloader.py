import pandas as pd
import os
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










    