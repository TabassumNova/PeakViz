import pandas as pd
import numpy as np
import os
from dataloader import *
from vizualization import *

if __name__ == "__main__":
    reflectance_paths = ['/Users/nova98/Documents/Nova/Spectrolysis/raw_data_car2car/PSR_FTIR/B_6_SSF/T8/FTIR/Reflectance/T8_S1_1_0000.txt']
    absorbance_paths = ['/Users/nova98/Documents/Nova/Spectrolysis/raw_data_car2car/PSR_FTIR/B_6_SSF/T8/FTIR/Absorbance/T8_S1_1_0000.txt']

    # data = Dataloader(reflectance_paths=reflectance_paths, absorbance_paths=absorption_paths)
    reflectance_df = load_reflectance(reflectance_paths)
    absorbance_df = load_absorbance(absorbance_paths)
    df_plot = {'T8_S1_1_0000.txt - Reflectance':reflectance_df,
                'T8_S1_1_0000.txt - Absorbance': absorbance_df
                }
    viz('test', df_plot, sensor='MWIR_LWIR')
    pass
