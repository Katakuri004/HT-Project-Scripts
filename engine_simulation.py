import numpy as np
from scipy.interpolate import interp1d

def wiebe_function(theta, theta_s, delta_theta, a=5, m=3):
    """
    Wiebe function for modeling the mass fraction burned during combustion.
    This is a well-established empirical model for heat release in IC engines.
    
    Parameters:
    -----------
    theta : float
        Current crank angle (degrees)
    theta_s : float
        Start of combustion (degrees)
    delta_theta : float
        Combustion duration (degrees)
    a : float
        Efficiency parameter (typically 5)
    m : float
        Shape parameter (typically 2-3)
    
    Returns:
    --------
    float
        Mass fraction burned (0 to 1)
    """
    if theta < theta_s:
        return 0
    x = (theta - theta_s) / delta_theta
    if x > 1:
        return 1
    return 1 - np.exp(-a * (x ** m))

def heat_loss_factor(theta, peak_temp, current_temp, ambient_temp):
    """
    Calculate heat loss factor based on temperature difference
    and crank angle position. Models heat transfer to cylinder walls.
    """
    base_loss = 0.02  # Base heat loss coefficient
    temp_factor = (current_temp - ambient_temp) / (peak_temp - ambient_temp)  # Temperature-dependent factor
    return base_loss * (1 + temp_factor)

def calculate_engine_cycle(n_points=720):
    """
    Calculate temperature and pressure throughout a 4-stroke engine cycle
    using thermodynamic principles and empirical models.
    
    Key assumptions and models used:
    1. Intake: Near-constant temperature and pressure
    2. Compression: Polytropic process (n=1.35)
    3. Combustion: Wiebe function for heat release with heat transfer
    4. Expansion: Polytropic process with variable gamma and heat transfer
    5. Exhaust: Two-phase model (blow-down + displacement)
    
    Parameters used are based on typical gasoline engine characteristics.
    """
    # Engine parameters (based on typical gasoline engine)
    compression_ratio = 10.0
    bore = 0.086  # m
    stroke = 0.086  # m
    con_rod_length = 0.143  # m
    
    # Ambient and initial conditions
    ambient_temp = 298  # K (25°C - typical ambient temperature)
    initial_temp = ambient_temp + 5  # K (Intake temperature slightly above ambient due to residual heat)
    initial_pressure = 101325  # Pa (1 atm)
    
    # Combustion parameters
    combustion_start = 345  # degrees (15° BTDC)
    combustion_duration = 60  # degrees
    peak_temp = 2500  # K (typical peak temperature)
    
    # Exhaust valve timing
    exhaust_valve_opening = 540  # Exhaust valve opens
    blowdown_duration = 30  # Duration of blow-down phase in degrees (shortened for more realistic behavior)
    
    # Create crank angle array
    crank_angles = np.linspace(0, 720, n_points)
    
    # Initialize arrays
    temperatures = np.zeros(n_points)
    pressures = np.zeros(n_points)
    volumes = np.zeros(n_points)
    
    # Pre-calculate target exhaust temperature
    exhaust_target_temp = ambient_temp * 1.15  # Slightly above ambient
    
    # Calculate instantaneous volume at each crank angle
    for i, theta in enumerate(crank_angles):
        theta_rad = np.radians(theta)
        # Volume calculation based on slider-crank mechanism
        term1 = 0.5 * (compression_ratio - 1)
        term2 = con_rod_length/stroke + 1 - np.cos(theta_rad)
        term3 = np.sqrt((con_rod_length/stroke)**2 - (np.sin(theta_rad))**2)
        volumes[i] = (1 + term1 * (term2 - term3))
    
    # Store reference conditions at start of compression
    v_ref = volumes[180]
    t_ref = initial_temp
    p_ref = initial_pressure
    
    # Calculate temperature and pressure for each stroke
    for i, theta in enumerate(crank_angles):
        if theta <= 180:  # Intake stroke
            # Slight pressure drop during intake
            temperatures[i] = initial_temp * 0.98  # Less temperature drop
            pressures[i] = initial_pressure * 0.95  # Less pressure drop
            
        elif theta <= 360:  # Compression stroke
            # Polytropic compression (n = 1.35)
            n = 1.35
            vol_ratio = volumes[i] / v_ref
            temperatures[i] = t_ref * (1/vol_ratio)**(n-1)
            pressures[i] = p_ref * (1/vol_ratio)**n
            
        elif theta <= exhaust_valve_opening:  # Combustion and expansion
            if combustion_start <= theta <= (combustion_start + combustion_duration):
                # Combustion phase using Wiebe function with heat transfer
                burn_fraction = wiebe_function(theta, combustion_start, combustion_duration)
                
                # Calculate temperature rise with heat transfer losses
                if i > 0:
                    heat_loss = heat_loss_factor(theta, peak_temp, temperatures[i-1], ambient_temp)
                    temp_rise = (peak_temp - temperatures[i-1]) * burn_fraction * (1 - heat_loss)
                    temperatures[i] = temperatures[i-1] + temp_rise
                    
                    # Calculate pressure considering both temperature and volume changes
                    vol_ratio = volumes[i] / volumes[i-1]
                    gamma = 1.35 - 0.05 * burn_fraction  # Variable gamma during combustion
                    pressures[i] = pressures[i-1] * (temperatures[i]/temperatures[i-1]) * (1/vol_ratio)**gamma
                else:
                    temperatures[i] = temperatures[i-1]
                    pressures[i] = pressures[i-1]
            else:
                # Expansion with heat transfer
                if i > 0:
                    # Variable polytropic exponent based on temperature
                    n = 1.3 - 0.05 * (temperatures[i-1] - ambient_temp) / (peak_temp - ambient_temp)
                    vol_ratio = volumes[i] / volumes[i-1]
                    
                    # Temperature calculation with heat transfer
                    heat_loss = heat_loss_factor(theta, peak_temp, temperatures[i-1], ambient_temp)
                    temperatures[i] = temperatures[i-1] * (vol_ratio)**(1-n) * (1 - heat_loss)
                    
                    # Pressure calculation
                    pressures[i] = pressures[i-1] * (temperatures[i]/temperatures[i-1]) * (1/vol_ratio)
                else:
                    temperatures[i] = temperatures[i-1]
                    pressures[i] = pressures[i-1]
                
        else:  # Exhaust stroke with blow-down modeling
            if theta <= (exhaust_valve_opening + blowdown_duration):
                # Blow-down phase: Rapid but controlled pressure and temperature drop
                progress = (theta - exhaust_valve_opening) / blowdown_duration
                
                # Calculate instantaneous target temperature that decreases with progress
                current_target = temperatures[i-1] * 0.7  # Target 70% of current temperature
                
                # Exponential decay for temperature
                decay_factor = np.exp(-2 * progress)  # Slower decay for temperature
                temperatures[i] = temperatures[i-1] * decay_factor + current_target * (1 - decay_factor)
                
                # Pressure calculation considering volume change
                vol_ratio = volumes[i] / volumes[i-1]
                # Faster pressure decay during blow-down
                pressure_target = initial_pressure * 1.1  # Slightly above atmospheric
                pressure_decay = np.exp(-4 * progress)
                pressures[i] = (pressures[i-1] * (temperatures[i]/temperatures[i-1]) * pressure_decay / vol_ratio + 
                              pressure_target * (1 - pressure_decay))
            else:
                # Displacement phase: Gradual approach to slightly above ambient conditions
                remaining_progress = (theta - (exhaust_valve_opening + blowdown_duration)) / (720 - (exhaust_valve_opening + blowdown_duration))
                
                # Smooth exponential decay to slightly above ambient
                if i > 0:
                    temp_diff = temperatures[i-1] - exhaust_target_temp
                    decay_rate = 0.08 * (1 + remaining_progress)  # Gradually increasing decay rate
                    temperatures[i] = temperatures[i-1] - temp_diff * decay_rate
                    
                    # Pressure follows temperature with volume consideration
                    vol_ratio = volumes[i] / volumes[i-1]
                    pressures[i] = pressures[i-1] * (temperatures[i]/temperatures[i-1]) / vol_ratio
                    # Ensure pressure stays within realistic bounds
                    pressures[i] = max(min(pressures[i], initial_pressure * 1.2), initial_pressure * 1.05)

    return crank_angles, temperatures - 273.15, pressures  # Convert temperatures to Celsius

if __name__ == "__main__":
    angles, temps, pressures = calculate_engine_cycle()
    print(f"Peak Temperature: {max(temps):.2f}°C")
    print(f"Peak Pressure: {max(pressures)/1e5:.2f} bar") 