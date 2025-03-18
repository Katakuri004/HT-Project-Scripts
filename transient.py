import numpy as np

class TransientAnalysis:
    def __init__(self):
        # Initial conditions and parameters
        self.initial_temperature = 25.0  # °C
        self.initial_pressure = 101325.0  # Pa (1 atm)
        self.ambient_temperature = 20.0  # °C
        self.heat_transfer_coefficient = 10.0  # W/m²·K
        self.volume = 1.0  # m³
        self.mass = 1.0  # kg
        self.specific_heat = 1000.0  # J/kg·K
        
    def calculate_temperature(self, time):
        """
        Calculate transient temperature using a simple heat transfer model
        T(t) = T_amb + (T_initial - T_amb) * exp(-hA*t/(m*cp))
        """
        # Calculate temperature decay
        temperature = (self.ambient_temperature + 
                      (self.initial_temperature - self.ambient_temperature) * 
                      np.exp(-self.heat_transfer_coefficient * time / 
                            (self.mass * self.specific_heat)))
        return temperature
    
    def calculate_pressure(self, time):
        """
        Calculate transient pressure using ideal gas law and temperature
        P(t) = P_initial * (T(t)/T_initial)
        """
        temperature = self.calculate_temperature(time)
        # Convert temperatures to Kelvin
        temp_kelvin = temperature + 273.15
        initial_temp_kelvin = self.initial_temperature + 273.15
        
        # Calculate pressure using ideal gas law
        pressure = self.initial_pressure * (temp_kelvin / initial_temp_kelvin)
        return pressure 