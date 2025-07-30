import pytest
import numpy as np
import pandas as pd
import os
from src import dataloader

def test_is_float():
    assert dataloader.is_float('1.23')
    assert not dataloader.is_float('abc')

def test_find_xy_reflectance():
    line = 'wavelength reflectance'
    x, y = dataloader.find_xy(line)
    assert x == 'wavelength' and y == 'reflectance'

def test_find_xy_absorbance():
    line = 'wavenumber absorbance'
    x, y = dataloader.find_xy(line)
    assert x == 'wavenumber' and y == 'absorbance'

def test_load_data(tmp_path):
    # Create a dummy reflectance file
    file_path = tmp_path / 'test.txt'
    with open(file_path, 'w') as f:
        f.write('wavelength reflectance\n')
        f.write('1000 0.1\n')
        f.write('1100 0.2\n')
    reflectance_df, absorbance_df = dataloader.load_data([str(file_path)], 'reflectance', 'wavelength reflectance')
    assert reflectance_df is not None
    assert absorbance_df is None
    assert 'sample' in reflectance_df.columns

def test_load_refSpectrum(tmp_path):
    file_path = tmp_path / 'ref.txt'
    with open(file_path, 'w') as f:
        f.write('sample 1000 0.1\n')
        f.write('sample 1100 0.2\n')
    df = dataloader.load_refSpectrum([str(file_path)])
    assert df is not None
    assert 'polymer' in df.columns or 'sample' in df.columns
