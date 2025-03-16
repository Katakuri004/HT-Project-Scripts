import numpy as np

def wiebe_function(theta, theta_s, delta_theta, a=5, m=3):
    """
    Wiebe function for modeling combustion heat release
    """
    if theta < theta_s:
        return 0
    x = (theta - theta_s) / delta_theta
    if x > 1:
        return 1
    return 1 - np.exp(-a * (x ** m))

def calculate_engine_cycle(n_points=720):
    """
    Calculate temperature and pressure throughout a 4-stroke engine cycle
    with simplified realistic effects
    """
    # Engine parameters
    compression_ratio = 10.0
    
    # Initial conditions
    ambient_temp = 298  # K (25°C)
    initial_temp = ambient_temp + 15  # K (Accounting for residual gases)
    initial_pressure = 101325  # Pa (1 atm)
    
    # Combustion parameters
    combustion_start = 355  # degrees (5° BTDC - later start for more realistic timing)
    combustion_duration = 40  # degrees (shorter duration for gasoline engine)
    peak_temp = 2800  # K (adjusted for better power curve)
    
    # Exhaust parameters
    exhaust_start = 540  # degrees
    blowdown_duration = 60  # degrees
    
    # Create arrays
    crank_angles = np.linspace(0, 720, n_points)
    temperatures = np.zeros(n_points)
    pressures = np.zeros(n_points)
    volumes = np.zeros(n_points)
    
    # Calculate volumes
    for i, theta in enumerate(crank_angles):
        # Simple volume calculation based on crank angle
        volumes[i] = 1 + 0.5 * (compression_ratio - 1) * (1 - np.cos(np.radians(theta)))
    
    # Reference conditions
    v_ref = volumes[180]  # End of intake
    t_ref = initial_temp
    p_ref = initial_pressure
    
    # Calculate cycle
    for i, theta in enumerate(crank_angles):
        if theta <= 180:  # Intake stroke
            temperatures[i] = initial_temp
            pressures[i] = initial_pressure * 0.95
            
        elif theta <= 360:  # Compression stroke
            n = 1.35
            vol_ratio = volumes[i] / v_ref
            temperatures[i] = t_ref * (1/vol_ratio)**(n-1)
            pressures[i] = p_ref * (1/vol_ratio)**n
            
        elif theta <= exhaust_start:  # Combustion and expansion
            if combustion_start <= theta <= (combustion_start + combustion_duration):
                # Combustion phase with more realistic heat release
                burn_fraction = wiebe_function(theta, combustion_start, combustion_duration)
                
                if i > 0:
                    # Variable heat loss based on temperature difference
                    temp_diff = temperatures[i-1] - ambient_temp
                    heat_loss = 0.15 + 0.05 * (temp_diff / peak_temp)  # Increased losses at higher temps
                    
                    # More gradual temperature rise
                    temp_rise = (peak_temp - temperatures[i-1]) * burn_fraction * (1 - heat_loss)
                    temperatures[i] = temperatures[i-1] + temp_rise
                    
                    # Pressure calculation with variable gamma
                    vol_ratio = volumes[i] / volumes[i-1]
                    gamma = 1.38 - 0.08 * (temperatures[i]/peak_temp)  # Variable gamma based on temperature
                    pressures[i] = pressures[i-1] * (temperatures[i]/temperatures[i-1]) * (1/vol_ratio)**gamma
                else:
                    temperatures[i] = temperatures[i-1]
                    pressures[i] = pressures[i-1]
            else:
                # Expansion phase with heat transfer
                if i > 0:
                    # Variable polytropic exponent based on temperature
                    temp_ratio = temperatures[i-1] / peak_temp
                    n = 1.3 - 0.05 * temp_ratio  # Lower exponent at higher temperatures
                    
                    # Volume ratio with limits for numerical stability
                    vol_ratio = volumes[i] / volumes[i-1]
                    
                    # Temperature calculation with heat loss
                    temp_diff = temperatures[i-1] - ambient_temp
                    heat_loss_factor = 0.02 * (temp_diff / peak_temp)  # Proportional to temperature difference
                    temperatures[i] = temperatures[i-1] * (vol_ratio)**(1-n) * (1 - heat_loss_factor)
                    
                    # Pressure calculation
                    pressures[i] = pressures[i-1] * (temperatures[i]/temperatures[i-1]) * (1/vol_ratio)
                else:
                    temperatures[i] = temperatures[i-1]
                    pressures[i] = pressures[i-1]
                
        else:  # Exhaust stroke
            if theta <= exhaust_start + blowdown_duration:
                if i > 0:
                    progress = (theta - exhaust_start) / blowdown_duration
                    decay = 1 / (1 + np.exp(6 * (progress - 0.5)))
                    
                    target_temp = initial_temp + 150
                    target_pressure = initial_pressure * 1.2
                    
                    temperatures[i] = (temperatures[i-1] * decay + 
                                    target_temp * (1 - decay))
                    
                    vol_ratio = volumes[i] / volumes[i-1]
                    base_pressure = pressures[i-1] * (temperatures[i]/temperatures[i-1]) / vol_ratio
                    pressures[i] = (base_pressure * decay + 
                                  target_pressure * (1 - decay))
            else:
                if i > 0:
                    remaining = (theta - (exhaust_start + blowdown_duration)) / (720 - (exhaust_start + blowdown_duration))
                    decay_rate = 0.02 + 0.03 * remaining
                    
                    target_temp = initial_temp + 120
                    temperatures[i] = temperatures[i-1] * (1 - decay_rate) + target_temp * decay_rate
                    
                    target_pressure = initial_pressure * 1.1
                    pressures[i] = pressures[i-1] * (1 - decay_rate) + target_pressure * decay_rate
    
    # Convert temperatures to Celsius
    temperatures = temperatures - 273.15
    
    return crank_angles, temperatures, pressures

if __name__ == "__main__":
    angles, temps, pressures = calculate_engine_cycle()
    print(f"Peak Temperature: {max(temps):.2f}°C")
    print(f"Peak Pressure: {max(pressures)/1e5:.2f} bar") 