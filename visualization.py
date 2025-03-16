import matplotlib.pyplot as plt
import numpy as np
from engine_simulation import calculate_engine_cycle

def plot_engine_cycle():
    """
    Create a detailed visualization of the 4-stroke engine cycle showing
    temperature and pressure variations with respect to crank angle.
    """
    # Calculate engine cycle data
    angles, temperatures, pressures = calculate_engine_cycle()
    
    # Set style for better visualization
    plt.style.use('default')  # Using default style
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    fig.patch.set_facecolor('white')  # Set white background
    
    fig.suptitle('4-Stroke IC Engine Cycle Analysis\n(Updated Model with Irreversible Effects)', 
                 fontsize=16, y=0.95)
    
    # Plot temperature
    ax1.plot(angles, temperatures, 'r-', linewidth=2.5, label='Temperature')
    ax1.set_title('Temperature vs Crank Angle', fontsize=14, pad=20)
    ax1.set_xlabel('Crank Angle (degrees)', fontsize=12)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('white')
    
    # Add stroke regions and labels for temperature plot
    strokes = ['Intake\n(0°-180°)', 'Compression\n(180°-360°)', 
               'Power\n(360°-540°)', 'Exhaust\n(540°-720°)']
    colors = ['lightblue', 'lightgreen', 'salmon', 'lightgray']
    
    for i, (stroke, color) in enumerate(zip(strokes, colors)):
        ax1.axvspan(i*180, (i+1)*180, alpha=0.2, color=color, label=stroke)
        ax1.text(i*180 + 90, ax1.get_ylim()[1]*0.9, stroke, 
                horizontalalignment='center', verticalalignment='center',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Add key events markers for temperature
    events = [
        (345, 'Combustion Start\n(345°)', 'red', '^'),
        (385, 'Peak Temperature\n(385°)', 'darkred', 'o'),
        (520, 'Exhaust Valve\nOpening (520°)', 'purple', 's')
    ]
    
    for angle, label, color, marker in events:
        temp_at_event = np.interp(angle, angles, temperatures)
        ax1.plot(angle, temp_at_event, marker=marker, color=color, markersize=10,
                label=label)
    
    # Plot pressure
    ax2.plot(angles, pressures/1e5, 'b-', linewidth=2.5, label='Pressure')
    ax2.set_title('Pressure vs Crank Angle', fontsize=14, pad=20)
    ax2.set_xlabel('Crank Angle (degrees)', fontsize=12)
    ax2.set_ylabel('Pressure (bar)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor('white')
    
    # Add stroke regions for pressure plot
    for i, (stroke, color) in enumerate(zip(strokes, colors)):
        ax2.axvspan(i*180, (i+1)*180, alpha=0.2, color=color)
        ax2.text(i*180 + 90, ax2.get_ylim()[1]*0.9, stroke,
                horizontalalignment='center', verticalalignment='center',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Add key events markers for pressure
    events = [
        (345, 'Combustion Start\n(345°)', 'blue', '^'),
        (375, 'Peak Pressure\n(375°)', 'darkblue', 'o'),
        (520, 'Exhaust Valve\nOpening (520°)', 'purple', 's')
    ]
    
    for angle, label, color, marker in events:
        pressure_at_event = np.interp(angle, angles, pressures)/1e5
        ax2.plot(angle, pressure_at_event, marker=marker, color=color, 
                markersize=10, label=label)
    
    # Add legends with better positioning
    ax1.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=10)
    ax2.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=10)
    
    # Add key metrics as text
    metrics_text = (
        f"Key Metrics:\n"
        f"Peak Temperature: {max(temperatures):.1f}°C\n"
        f"Min Temperature: {min(temperatures):.1f}°C\n"
        f"Avg Temperature: {np.mean(temperatures):.1f}°C\n\n"
        f"Peak Pressure: {max(pressures)/1e5:.1f} bar\n"
        f"Min Pressure: {min(pressures)/1e5:.1f} bar\n"
        f"Avg Pressure: {np.mean(pressures)/1e5:.1f} bar"
    )
    
    plt.figtext(0.02, 0.02, metrics_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 0.85, 0.95])
    
    # Display maximum values
    print(f"Peak Temperature: {max(temperatures):.1f}°C")
    print(f"Peak Pressure: {max(pressures)/1e5:.1f} bar")
    
    plt.show()

if __name__ == "__main__":
    plot_engine_cycle() 