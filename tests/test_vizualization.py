import pytest
import numpy as np
import pandas as pd
import os
from src import vizualization

def test_hex_rgba():
    # Test the hex_rgba function for correct rgba output
    hex_color = '#FF0000'
    transparency = 0.5
    expected = (255, 0, 0, 0.5)
    result = vizualization.hex_rgba(hex_color, transparency)
    assert result == expected

def test_create_masked_image(tmp_path, monkeypatch):
    # Create dummy RGB and mask files
    import cv2
    rgb = np.ones((60, 60, 3), dtype=np.uint8) * 255
    mask = np.zeros((10, 10, 1), dtype=np.uint8)
    mask[2:8, 2:8, 0] = 1
    rgb_path = tmp_path / 'RGB.png'
    mask_path = tmp_path / 'mask.hdr'
    cv2.imwrite(str(rgb_path), rgb)
    # Patch io.load to return a dummy object with .data
    class DummyMask:
        def __init__(self, data):
            self.data = data
    monkeypatch.setattr(vizualization.io, 'load', lambda path: DummyMask(mask))
    vizualization.create_masked_image(str(tmp_path))
    assert os.path.exists(tmp_path / 'RGB_masked.png')

def test_viz(monkeypatch):
    # Test viz function with minimal DataFrame
    df = pd.DataFrame({
        'sample': ['A', 'B'],
        1000: [0.1, 0.2],
        1100: [0.2, 0.3]
    })
    df_plot = {'test': [df, 'Reflectance']}
    # Patch fig.show to avoid opening browser
    monkeypatch.setattr(vizualization.go.Figure, 'show', lambda self: None)
    vizualization.viz('batch', df_plot, sensor='imaging', download=False)

def test_viz_image_data(monkeypatch, tmp_path):
    # Test viz_image_data with dummy hylib_dict
    df = pd.DataFrame(np.random.rand(5, 5), columns=[str(i) for i in range(5)])
    hylib_dict = {'test': df}
    # Patch fig.show to avoid opening browser
    monkeypatch.setattr(vizualization.go.Figure, 'show', lambda self: None)
    vizualization.viz_image_data('batch', hylib_dict, str(tmp_path), sensor='imaging', download=False)
