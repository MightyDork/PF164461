import unittest
from lab2.src.temperature_converter import TemperatureConverter

class TestTemperatureConverter(unittest.TestCase):
    def setUp(self):
        self.temperature_converter = TemperatureConverter()

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(self.temperature_converter.celsius_to_kelvin(0),-273.15)

    def tearDown(self):
        pass