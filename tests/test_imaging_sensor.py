import pytest
import numpy as np
import pandas as pd
from src import imaging_sensor

def test_imaging_sensor_init():
    sensor = imaging_sensor.ImagingSensor()
    assert hasattr(sensor, 'widget1')
    assert hasattr(sensor, 'hylib_dict')
    assert sensor.hylib_dict is None

def test_select_absorbance(monkeypatch):
    sensor = imaging_sensor.ImagingSensor()
    sensor.hylib_dict = {'dummy': pd.DataFrame(np.random.rand(2, 2))}
    sensor.checkBoxAbsorbance = type('obj', (), {'isChecked': lambda self: True})()
    sensor.sender = lambda: sensor.checkBoxAbsorbance
    # Patch convert_absorbance to check if called
    called = {}
    def fake_convert():
        called['yes'] = True
    sensor.convert_absorbance = fake_convert
    sensor.select_absorbance(Qt.Checked)
    assert called.get('yes')
