import numpy as np
import pandas as pd

# Given Constants
P_ref = 101325  # Atmospheric pressure in Pa
T_ambient = 350  # Typical engine block ambient temperature in Kelvin
T_peak = 1026.85  # Given peak temperature in Kelvin
V_ref = 500e-6  # Reference volume (BDC) in cubic meters (0.5 L)
V_c = 50e-6  # Clearance volume in cubic meters (0.05 L)
n = 1.35  # Polytropic index

# Engine Specifications
N = 1000  # Engine speed in RPM
omega = (N / 60) * 360  # Angular velocity in degrees per second

# Crank and connecting rod parameters
S = 80e-3  # Stroke length in meters
D = 80e-3  # Bore diameter in meters
r = S / 2  # Crank radius in meters
l = 1.5 * r  # Connecting rod length

# Peak combustion parameters
P_max = 3.5e6  # Peak combustion pressure in Pa
theta_start_comb = 360  # Start of combustion in degrees
theta_end_comb = 390  # End of combustion in degrees
a_weibe = 5  # Weibe function parameter
m_weibe = 2  # Weibe function parameter

# Generate crank angles from 0 to 720 degrees in steps of 10
crank_angles = np.arange(0, 721, 10)

# Initialize lists to store results
time_steps = []
temperatures = []
pressures = []

# Calculate time step for each crank angle
for theta in crank_angles:
    time = theta / omega  # Time in seconds
    
    # Compute cylinder volume at crank angle theta
    V_theta = V_c + (np.pi * D**2 / 4) * (r * (1 - np.cos(np.radians(theta))) + (r**2 / l) * (1 - np.cos(2 * np.radians(theta))))
    
    # Compression and Expansion temperature calculation using polytropic relation
    if theta < 360:  # Compression stroke
        T_theta = T_ambient * (V_ref / V_theta) ** (n - 1)
    elif 360 <= theta <= 390:  # Combustion phase (using linear assumption)
        T_theta = T_peak * ((theta - 360) / (390 - 360)) + T_ambient * (1 - (theta - 360) / (390 - 360))
    else:  # Expansion stroke
        T_theta = T_peak * (V_theta / V_ref) ** (n - 1)
    
    # Compression and Expansion pressure calculation using polytropic relation
    if theta < 360:  # Compression stroke
        P_theta = P_ref * (V_ref / V_theta) ** n
    elif 360 <= theta <= 390:  # Combustion phase (using Weibe function approximation)
        P_theta = P_max * np.exp(-a_weibe * ((theta - 360) / (390 - 360)) ** m_weibe)
    else:  # Expansion stroke
        P_theta = P_max * (V_theta / V_ref) ** n
    
    # Store results
    time_steps.append(time)
    temperatures.append(T_theta)
    pressures.append(P_theta)

# Create DataFrame
df = pd.DataFrame({
    "Crank Angle (deg)": crank_angles,
    "Time (s)": time_steps,
    "Temperature (K)": temperatures,
    "Pressure (Pa)": pressures
})

# Save to Excel
df.to_excel("time_dependent_temp_pressure_1000RPM.xlsx", index=False)
