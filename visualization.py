import matplotlib.pyplot as plt
from engine_simulation import calculate_engine_cycle
import numpy as np

def plot_engine_cycle():
    """
    Create a detailed visualization of the 4-stroke engine cycle showing
    temperature and pressure variations with respect to crank angle.
    """
    # Calculate engine cycle data
    angles, temperatures, pressures = calculate_engine_cycle()
    
    # Set style for better visualization
    plt.style.use('bmh')
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    fig.suptitle('4-Stroke IC Engine Cycle Analysis', fontsize=16, y=0.95)
    
    # Plot temperature
    ax1.plot(angles, temperatures, 'r-', linewidth=2, label='Temperature')
    ax1.set_title('Temperature vs Crank Angle')
    ax1.set_xlabel('Crank Angle (degrees)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True, alpha=0.3)
    
    # Add stroke regions and labels for temperature plot
    strokes = ['Intake', 'Compression', 'Power\n(Combustion + Expansion)', 'Exhaust']
    colors = ['lightblue', 'lightgreen', 'salmon', 'lightgray']
    
    for i, (stroke, color) in enumerate(zip(strokes, colors)):
        ax1.axvspan(i*180, (i+1)*180, alpha=0.2, color=color, label=stroke)
        ax1.text(i*180 + 90, ax1.get_ylim()[1]*0.9, stroke, 
                horizontalalignment='center', verticalalignment='center')
    
    # Add key events markers for temperature
    events = [
        (345, 'Combustion\nStart', 'red', '^'),
        (385, 'Peak\nTemperature', 'darkred', 'o')
    ]
    
    for angle, label, color, marker in events:
        temp_at_event = np.interp(angle, angles, temperatures)
        ax1.plot(angle, temp_at_event, marker=marker, color=color, markersize=10,
                label=label)
    
    # Plot pressure
    ax2.plot(angles, pressures/1e5, 'b-', linewidth=2, label='Pressure')
    ax2.set_title('Pressure vs Crank Angle')
    ax2.set_xlabel('Crank Angle (degrees)')
    ax2.set_ylabel('Pressure (bar)')
    ax2.grid(True, alpha=0.3)
    
    # Add stroke regions for pressure plot
    for i, (stroke, color) in enumerate(zip(strokes, colors)):
        ax2.axvspan(i*180, (i+1)*180, alpha=0.2, color=color)
        ax2.text(i*180 + 90, ax2.get_ylim()[1]*0.9, stroke,
                horizontalalignment='center', verticalalignment='center')
    
    # Add key events markers for pressure
    events = [
        (345, 'Combustion\nStart', 'blue', '^'),
        (375, 'Peak\nPressure', 'darkblue', 'o')
    ]
    
    for angle, label, color, marker in events:
        pressure_at_event = np.interp(angle, angles, pressures)/1e5
        ax2.plot(angle, pressure_at_event, marker=marker, color=color, 
                markersize=10, label=label)
    
    # Add legends
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Adjust layout to prevent label overlap
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    # Display maximum values
    print(f"Peak Temperature: {max(temperatures):.1f}°C")
    print(f"Peak Pressure: {max(pressures)/1e5:.1f} bar")
    
    plt.show()

if __name__ == "__main__":
    plot_engine_cycle() 