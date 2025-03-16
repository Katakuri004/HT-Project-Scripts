import numpy as np
import pandas as pd
from engine_simulation import calculate_engine_cycle

def generate_engine_data(rpm=1200, sample_interval=1):
    """
    Generate engine cycle data with precise timing at specified RPM
    
    Parameters:
    -----------
    rpm : int
        Engine speed in revolutions per minute
    sample_interval : int
        Crank angle interval for data sampling (degrees)
    
    Returns:
    --------
    DataFrame with time, crank angle, temperature, and pressure data
    """
    # Calculate time per revolution
    seconds_per_rev = 60 / rpm
    
    # Get engine cycle data
    angles, temperatures, pressures = calculate_engine_cycle(n_points=720)
    
    # Create time array (two revolutions for 4-stroke cycle)
    total_time = 2 * seconds_per_rev
    times = np.array([round(angle * total_time / 720, 6) for angle in angles])
    
    # Create DataFrame with all data points
    df_all = pd.DataFrame({
        'Time (s)': times,
        'Crank Angle (deg)': angles,
        'Temperature (°C)': temperatures,
        'Pressure (bar)': pressures / 1e5
    })
    
    # Create DataFrame with sampled data (every sample_interval degrees)
    sampled_indices = np.arange(0, len(angles), sample_interval)
    df_sampled = df_all.iloc[sampled_indices].copy()
    
    return df_all, df_sampled

def save_to_excel(rpm=1200):
    """
    Save engine data to Excel files
    - One file with data for every degree
    - One file with data every 10 degrees
    """
    # Generate data
    df_detailed, df_sampled = generate_engine_data(rpm=rpm, sample_interval=10)
    
    # Save detailed data (every degree)
    detailed_filename = f'engine_data_{rpm}rpm_detailed.xlsx'
    df_detailed.to_excel(detailed_filename, index=False, float_format='%.4f')
    
    # Save sampled data (every 10 degrees)
    sampled_filename = f'engine_data_{rpm}rpm_10deg.xlsx'
    df_sampled.to_excel(sampled_filename, index=False, float_format='%.4f')
    
    print(f"Generated files:")
    print(f"1. {detailed_filename} - Data for every crank angle degree")
    print(f"2. {sampled_filename} - Data every 10 degrees")
    
    # Print some key metrics
    print("\nKey Metrics:")
    print(f"Engine Speed: {rpm} RPM")
    print(f"Cycle Time: {120/rpm:.4f} seconds")
    print(f"Peak Temperature: {df_detailed['Temperature (°C)'].max():.1f}°C")
    print(f"Peak Pressure: {df_detailed['Pressure (bar)'].max():.1f} bar")

if __name__ == "__main__":
    save_to_excel(rpm=1200) 