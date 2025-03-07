class TemperatureConverter:

    def celsius_to_kelvin(self, celsius):
        return celsius-273.15

    def kelvin_to_celsius(self, kelvin):
        return kelvin+273.15

    def celsius_to_fahrenheit(self, celsius):
        return ((9/5) * celsius) + 32