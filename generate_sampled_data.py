import pandas as pd
import numpy as np
from engine_simulation import calculate_engine_cycle
from openpyxl.utils import get_column_letter

def generate_sampled_data_excel(output_file='engine_sampled_results.xlsx', engine_rpm=3000):
    """
    Generate an Excel file containing engine simulation results sampled at 10-degree intervals,
    resulting in exactly 72 data points for a complete cycle (720 degrees).
    
    Parameters:
    -----------
    output_file : str
        Name of the output Excel file
    engine_rpm : int
        Engine speed in revolutions per minute (default: 3000 RPM)
    """
    # Set pandas display options for floating point numbers
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    
    # Calculate engine cycle data
    angles, temperatures, pressures = calculate_engine_cycle()
    
    # Create interpolation functions for temperature and pressure
    angle_points = np.linspace(0, 720, len(angles))
    temp_interp = np.interp(np.arange(0, 720, 10), angle_points, temperatures)
    press_interp = np.interp(np.arange(0, 720, 10), angle_points, pressures)
    
    # Generate sampled crank angles (0, 10, 20, ..., 710)
    sampled_angles = np.arange(0, 720, 10)
    
    # Calculate time data for sampled points with higher precision
    # For one complete cycle (720 degrees), time = (720/360)*(1/RPM)*60 seconds
    cycle_time = (720/360) * (1/engine_rpm) * 60  # Total time for one cycle in seconds
    sampled_times = np.linspace(0, cycle_time, 72)  # 72 equally spaced time points
    
    # Create a DataFrame with the sampled results
    data = {
        'Time (seconds)': sampled_times,
        'Crank Angle (degrees)': sampled_angles,
        'Temperature (°C)': temp_interp,
        'Pressure (bar)': press_interp / 1e5  # Convert Pa to bar
    }
    df = pd.DataFrame(data)
    
    # Add stroke information
    strokes = []
    for angle in sampled_angles:
        if 0 <= angle < 180:
            strokes.append('Intake')
        elif 180 <= angle < 360:
            strokes.append('Compression')
        elif 360 <= angle < 540:
            strokes.append('Power')
        else:
            strokes.append('Exhaust')
    df['Stroke'] = strokes
    
    # Calculate key metrics
    metrics = {
        'Metric': [
            'Engine Speed',
            'Cycle Duration',
            'Number of Sample Points',
            'Sampling Interval',
            'Peak Temperature',
            'Minimum Temperature',
            'Peak Pressure',
            'Minimum Pressure',
            'Average Temperature',
            'Average Pressure'
        ],
        'Value': [
            f"{engine_rpm} RPM",
            f"{cycle_time:.4f} seconds",
            "72 points",
            "10 degrees",
            f"{max(temp_interp):.4f} °C",
            f"{min(temp_interp):.4f} °C",
            f"{max(press_interp/1e5):.4f} bar",
            f"{min(press_interp/1e5):.4f} bar",
            f"{np.mean(temp_interp):.4f} °C",
            f"{np.mean(press_interp/1e5):.4f} bar"
        ]
    }
    metrics_df = pd.DataFrame(metrics)
    
    # Create stroke summary with higher precision
    stroke_summary = df.groupby('Stroke').agg({
        'Temperature (°C)': ['mean', 'min', 'max'],
        'Pressure (bar)': ['mean', 'min', 'max']
    }).round(4)
    
    # Create Excel writer object with number formatting
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write the main simulation data with 4 decimal places
        df.style.format({
            'Time (seconds)': '{:.4f}',
            'Temperature (°C)': '{:.4f}',
            'Pressure (bar)': '{:.4f}'
        }).to_excel(writer, sheet_name='Sampled Data', index=False)
        
        # Write the metrics summary
        metrics_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Write the stroke summary
        stroke_summary.to_excel(writer, sheet_name='Stroke Analysis')
        
        # Auto-adjust columns width for each sheet
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for i, col in enumerate(df.columns if sheet_name == 'Sampled Data' 
                                  else metrics_df.columns if sheet_name == 'Summary'
                                  else stroke_summary.columns, 1):
                column_letter = get_column_letter(i)
                # Make columns wider to accommodate more decimal places
                worksheet.column_dimensions[column_letter].width = 18

if __name__ == "__main__":
    # Generate data for different engine speeds
    rpms = [1000, 2000, 3000, 4000, 5000]
    for rpm in rpms:
        output_file = f'engine_sampled_results_{rpm}rpm.xlsx'
        generate_sampled_data_excel(output_file=output_file, engine_rpm=rpm)
        print(f"Excel file for {rpm} RPM has been generated successfully!") 