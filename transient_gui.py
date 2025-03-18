import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from engine_simulation import calculate_engine_cycle

class EngineSimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Engine Cycle Simulation GUI")
        self.root.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Input Parameters", padding="5")
        self.input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Number of steps input with range info
        ttk.Label(self.input_frame, text="Number of Steps (n) [10-720]:").grid(row=0, column=0, padx=5)
        self.n_steps = ttk.Entry(self.input_frame, width=10)
        self.n_steps.grid(row=0, column=1, padx=5)
        self.n_steps.insert(0, "72")  # Default value (every 10 degrees)
        
        # Add RPM input
        ttk.Label(self.input_frame, text="Engine Speed (RPM):").grid(row=0, column=3, padx=5)
        self.rpm_entry = ttk.Entry(self.input_frame, width=10)
        self.rpm_entry.grid(row=0, column=4, padx=5)
        self.rpm_entry.insert(0, "1200")  # Default RPM
        
        # Add description labels
        description = "n = number of equidistant points (e.g., 720 = every 1°, 72 = every 10°)"
        ttk.Label(self.input_frame, text=description, font=('Arial', 8)).grid(row=1, column=0, columnspan=3, pady=(0,5))
        
        rpm_desc = "Engine speed affects time calculations"
        ttk.Label(self.input_frame, text=rpm_desc, font=('Arial', 8)).grid(row=1, column=3, columnspan=2, pady=(0,5))
        
        # Generate button
        self.generate_btn = ttk.Button(self.input_frame, text="Generate", command=self.generate_data)
        self.generate_btn.grid(row=0, column=2, padx=5)
        
        # Create figure for plots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Save button
        self.save_btn = ttk.Button(self.main_frame, text="Save to Excel", command=self.save_to_excel)
        self.save_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Initialize data storage
        self.temperature_data = None
        self.pressure_data = None
        self.angle_data = None
        self.time_data = None
        self.rpm = None

    def calculate_time_data(self):
        """Calculate time data based on crank angle and RPM"""
        if self.rpm and self.angle_data is not None:
            # Time for one complete cycle (2 revolutions for 4-stroke)
            cycle_time = (60 / self.rpm) * 2  # seconds
            # Calculate time for each angle
            self.time_data = self.angle_data * cycle_time / 720

    def generate_data(self):
        try:
            # Get and validate input
            value = self.n_steps.get()
            if not value.isdigit():
                raise ValueError("Please enter a valid number for steps")
            
            rpm_value = self.rpm_entry.get()
            if not rpm_value.isdigit():
                raise ValueError("Please enter a valid number for RPM")
            
            n = int(value)
            self.rpm = int(rpm_value)
            
            if n < 10 or n > 720:
                raise ValueError("Number of steps must be between 10 and 720")
            if self.rpm < 1:
                raise ValueError("RPM must be positive")
            
            # First get high-resolution data
            angles_full, temps_full, press_full = calculate_engine_cycle(n_points=720)
            
            # Create interpolated points based on n
            step_size = 720 / n
            self.angle_data = np.linspace(0, 720, n)
            
            # Interpolate temperature and pressure data
            self.temperature_data = np.interp(self.angle_data, angles_full, temps_full)
            self.pressure_data = np.interp(self.angle_data, angles_full, press_full)
            
            # Calculate time data
            self.calculate_time_data()
            
            # Update plots
            self.update_plots()
            
            # Show step size in the success message
            messagebox.showinfo("Success", 
                              f"Data generated successfully!\nStep size: {step_size:.1f}° between points")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_plots(self):
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Calculate marker size based on number of points
        n_points = len(self.angle_data)
        marker_size = max(5, min(50, 500 / n_points))  # Adjust marker size based on number of points
        
        # Plot temperature with both line and markers
        self.ax1.plot(self.angle_data, self.temperature_data, 'r-', label='Temperature', zorder=1)
        self.ax1.plot(self.angle_data, self.temperature_data, 'ko', label='Data Points', 
                     markersize=marker_size, markerfacecolor='white', markeredgewidth=1, zorder=2)
        self.ax1.set_xlabel('Crank Angle (degrees)')
        self.ax1.set_ylabel('Temperature (°C)')
        self.ax1.set_title('Temperature vs Crank Angle')
        self.ax1.grid(True)
        
        # Add stroke regions and labels for temperature plot
        strokes = ['Intake\n(0°-180°)', 'Compression\n(180°-360°)', 
                  'Power\n(360°-540°)', 'Exhaust\n(540°-720°)']
        colors = ['lightblue', 'lightgreen', 'salmon', 'lightgray']
        
        for i, (stroke, color) in enumerate(zip(strokes, colors)):
            self.ax1.axvspan(i*180, (i+1)*180, alpha=0.2, color=color, label=stroke)
            self.ax1.text(i*180 + 90, self.ax1.get_ylim()[1]*0.9, stroke, 
                    horizontalalignment='center', verticalalignment='center',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Plot pressure with both line and markers
        self.ax2.plot(self.angle_data, self.pressure_data/1e5, 'b-', label='Pressure', zorder=1)
        self.ax2.plot(self.angle_data, self.pressure_data/1e5, 'ko', label='Data Points',
                     markersize=marker_size, markerfacecolor='white', markeredgewidth=1, zorder=2)
        self.ax2.set_xlabel('Crank Angle (degrees)')
        self.ax2.set_ylabel('Pressure (bar)')
        self.ax2.set_title('Pressure vs Crank Angle')
        self.ax2.grid(True)
        
        # Add stroke regions for pressure plot
        for i, (stroke, color) in enumerate(zip(strokes, colors)):
            self.ax2.axvspan(i*180, (i+1)*180, alpha=0.2, color=color)
            self.ax2.text(i*180 + 90, self.ax2.get_ylim()[1]*0.9, stroke,
                    horizontalalignment='center', verticalalignment='center',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Set x-axis limits to exactly 0-720 degrees
        self.ax1.set_xlim(0, 720)
        self.ax2.set_xlim(0, 720)
        
        # Add legends
        self.ax1.legend(loc='upper right')
        self.ax2.legend(loc='upper right')
        
        # Adjust layout and update canvas
        self.fig.tight_layout()
        self.canvas.draw()
    
    def save_to_excel(self):
        if self.temperature_data is None or self.pressure_data is None:
            messagebox.showerror("Error", "No data to save. Please generate data first.")
            return
            
        try:
            # Create DataFrame with time data
            df = pd.DataFrame({
                'Time (s)': self.time_data,
                'Crank Angle (degrees)': self.angle_data,
                'Temperature (°C)': self.temperature_data,
                'Pressure (bar)': self.pressure_data / 1e5
            })
            
            # Get the step size
            n = len(self.angle_data)
            step_size = 720 / n
            
            # Save to Excel with step size and RPM in filename
            filename = f"engine_cycle_data_{step_size:.1f}deg_step_{self.rpm}rpm.xlsx"
            
            # Configure Excel writer to format time with 4 decimal places
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                worksheet = writer.sheets['Sheet1']
                # Format time column to 4 decimal places
                for idx, col in enumerate(df.columns):
                    if col == 'Time (s)':
                        for row in range(2, len(df) + 2):  # Excel is 1-indexed and has header
                            cell = worksheet.cell(row=row, column=idx+1)
                            cell.number_format = '0.0000'
            
            messagebox.showinfo("Success", f"Data saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EngineSimulationGUI(root)
    root.mainloop() 