import numpy as np
import pandas as pd
from engine_simulation import calculate_engine_cycle

def generate_engine_data(rpm=1200):
    """
    Generate engine cycle data with precise timing at specified RPM
    
    Parameters:
    -----------
    rpm : int
        Engine speed in revolutions per minute
    
    Returns:
    --------
    DataFrame with time, crank angle, temperature, and pressure data at 10-degree intervals
    """
    # Calculate time per revolution
    seconds_per_rev = 60 / rpm
    
    # Get engine cycle data
    angles, temperatures, pressures = calculate_engine_cycle(n_points=720)
    
    # Create time array (two revolutions for 4-stroke cycle)
    total_time = 2 * seconds_per_rev
    
    # Sample at 10-degree intervals
    sampled_indices = np.arange(0, len(angles), 10)
    sampled_angles = angles[sampled_indices]
    
    # Calculate precise time values with exactly 4 decimal places
    times = np.array([round(angle * total_time / 720, 4) for angle in sampled_angles])
    
    # Create DataFrame with sampled data
    df = pd.DataFrame({
        'Time (s)': times,
        'Crank Angle (deg)': sampled_angles,
        'Temperature (°C)': temperatures[sampled_indices],
        'Pressure (bar)': pressures[sampled_indices] / 1e5
    })
    
    return df

def save_to_excel(rpm=1200):
    """
    Save engine data to Excel file with 10-degree intervals
    """
    # Generate data
    df = generate_engine_data(rpm=rpm)
    
    # Save data with exactly 4 decimal places
    filename = 'engine_data_10deg_precise.xlsx'
    
    # Configure Excel writer to use specific number formats
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # Format time column to exactly 4 decimal places
        for idx, col in enumerate(df.columns):
            if col == 'Time (s)':
                for row in range(2, len(df) + 2):  # Excel is 1-indexed and has header
                    cell = worksheet.cell(row=row, column=idx+1)
                    cell.number_format = '0.0000'
            elif col in ['Temperature (°C)', 'Pressure (bar)']:
                for row in range(2, len(df) + 2):
                    cell = worksheet.cell(row=row, column=idx+1)
                    cell.number_format = '0.00'
    
    print(f"Generated file: {filename}")
    print("\nKey Metrics:")
    print(f"Engine Speed: {rpm} RPM")
    print(f"Cycle Time: {120/rpm:.4f} seconds")
    print(f"Time step (10 degrees): {(120/rpm/720*10):.4f} seconds")
    print(f"Peak Temperature: {df['Temperature (°C)'].max():.2f}°C")
    print(f"Peak Pressure: {df['Pressure (bar)'].max():.2f} bar")
    print(f"\nNumber of data points: {len(df)} (every 10 degrees)")

if __name__ == "__main__":
    save_to_excel(rpm=1200) 