import numpy as np
import pandas as pd
import os

def rescale_data(df):
    new = []
    for index, row in df.iterrows():
        text = [row.iloc[0]]
        energy = np.array(row)[1:]
        min_val = energy.min()
        max_val = energy.max()
        rescaled_energy = list((energy - min_val) / (max_val - min_val))
        new.append(text+rescaled_energy)

    rescaled_df = pd.DataFrame(new, columns=list(df.columns))
    return rescaled_df

def common_prefix(strings):
    if not strings:
        return ""
    
    # Find the length of the shortest string
    min_length = min(len(s) for s in strings)
    
    # Compare characters
    for i in range(min_length):
        if len(set(s[i] for s in strings)) > 1:
            return strings[0][:i]
    
    # If we've made it here, return the whole shortest string
    return strings[0][:min_length]

def average_data(df, input_path, signal_type):
    samples = list(df['sample'])
    averaged_name = common_prefix(samples)
    averaged_list = []
    for (columnName, columnData) in df.items(): 
        is_float = np.issubdtype(columnData.dtype, np.floating)
        if is_float:
            mean = columnData.mean().item()
            averaged_list.append(mean)
    averaged_df1 = pd.DataFrame([averaged_list], columns=list(df.columns[1:]))

    ### For generating text file
    reshaped_df = averaged_df1.melt(var_name="Wavelength (nm)", value_name="FTIR signal").reset_index(drop=True)
    file_path, folder = os.path.split(input_path)
    output_path = os.path.join(file_path, averaged_name+ signal_type + '.txt')
    with open(output_path, 'w') as f:
        f.write("XYUNITS Nanometer; "+ signal_type + "\n")
        reshaped_df.to_csv(f, sep=' ', index=False, header=True)

    averaged_df2 = pd.DataFrame([[averaged_name]+averaged_list], columns=list(df.columns))
    return averaged_df2
