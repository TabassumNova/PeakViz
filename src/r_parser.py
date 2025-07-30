import pandas as pd
import re

def parse_r_script(file_path):
    data = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            # Match lines that define variables
            match = re.match(r'([\w\.]+)\s*(=|<-)\s*c\((.*)\)', line.strip())
            # match = re.match(r'(\w+)\s*(=|<-)\s*c\((.*)\)', line.strip())
            if match:
                var_name = match.group(1)
                values = match.group(3)
                # Convert the values to a list of integers
                values_list = [int(v.strip()) for v in values.split(',')]
                data[var_name] = values_list
    
    # Find the maximum length of the lists
    max_length = max(len(lst) for lst in data.values())
    
    # Pad the lists with None to make them the same length
    for key in data:
        data[key].extend([None] * (max_length - len(data[key])))
    
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    
    return df

# Example usage
file_path = '/Users/nova98/Documents/Nova/Spectrolysis/raw_data_car2car/PSR_FTIR_library/FTIR_spectral-fingerprints.R'
df = parse_r_script(file_path)
print(df)