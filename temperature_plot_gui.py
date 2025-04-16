import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np
import math

class TemperaturePlotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Data Plotter")
        self.root.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection frame
        self.file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="5")
        self.file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # File path display
        self.file_path = tk.StringVar()
        self.file_path_entry = ttk.Entry(self.file_frame, textvariable=self.file_path, width=60)
        self.file_path_entry.grid(row=0, column=0, padx=5, pady=5)
        
        # Browse button
        self.browse_btn = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_btn.grid(row=0, column=1, padx=5)
        
        # Load button
        self.load_btn = ttk.Button(self.file_frame, text="Load & Plot", command=self.load_and_plot)
        self.load_btn.grid(row=0, column=2, padx=5)

        # Heat Flux Parameters Frame
        self.params_frame = ttk.LabelFrame(self.main_frame, text="Heat Flux Parameters", padding="5")
        self.params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Piston diameter input
        ttk.Label(self.params_frame, text="Piston Head Diameter (m):").grid(row=0, column=0, padx=5, pady=5)
        self.diameter_var = tk.StringVar(value="0.1")  # Default 10cm diameter
        self.diameter_entry = ttk.Entry(self.params_frame, textvariable=self.diameter_var, width=10)
        self.diameter_entry.grid(row=0, column=1, padx=5, pady=5)

        # Multiple thermal conductivity inputs
        ttk.Label(self.params_frame, text="Thermal Conductivities (W/m·K):").grid(row=0, column=2, padx=5, pady=5)
        self.k_var = tk.StringVar(value="50, 100, 150")  # Default values
        self.k_entry = ttk.Entry(self.params_frame, textvariable=self.k_var, width=20)
        self.k_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Add helper text for k values
        ttk.Label(self.params_frame, text="(Enter comma-separated values)").grid(row=1, column=2, columnspan=2, padx=5)
        
        # Add file format info
        file_info = ("Expected file format:\n"
                    "CSV or Excel file with columns:\n"
                    "- Time [s]\n"
                    "- Minimum [°C]\n"
                    "- Maximum [°C]\n"
                    "- Average [°C]")
        ttk.Label(self.file_frame, text=file_info, justify=tk.LEFT).grid(
            row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        
        # Create notebook for multiple plots
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Temperature plot frame
        self.temp_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.temp_frame, text='Temperature Plot')

        # Heat flux plot frame
        self.flux_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.flux_frame, text='Heat Flux Plot')
        
        # Create figures for plots
        self.fig_temp, self.ax_temp = plt.subplots(figsize=(10, 6))
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.temp_frame)
        self.canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig_flux, self.ax_flux = plt.subplots(figsize=(10, 6))
        self.canvas_flux = FigureCanvasTkAgg(self.fig_flux, master=self.flux_frame)
        self.canvas_flux.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def parse_k_values(self):
        """Parse comma-separated k values and return as list of floats"""
        try:
            k_values = [float(k.strip()) for k in self.k_var.get().split(',')]
            if not k_values:
                raise ValueError("Please enter at least one thermal conductivity value")
            return k_values
        except ValueError as e:
            raise ValueError("Invalid thermal conductivity values. Please enter comma-separated numbers")

    def calculate_heat_flux(self, df, k_value):
        """Calculate heat flux for a single k value"""
        try:
            diameter = float(self.diameter_var.get())
            
            # Calculate area
            area = math.pi * (diameter/2)**2
            
            # Calculate temperature difference (ΔT)
            delta_t = df['Maximum [°C]'] - df['Minimum [°C]']
            
            # Calculate heat flux (q = -k * ΔT/Δx)
            thickness = 0.001  # 1mm in meters
            heat_flux = k_value * delta_t / thickness
            
            # Calculate total heat transfer rate (Q = q * A)
            heat_transfer_rate = heat_flux * area
            
            return heat_flux, heat_transfer_rate
            
        except ValueError as e:
            raise ValueError("Please enter a valid numerical value for diameter")

    def browse_file(self):
        filetypes = (
            ('CSV files', '*.csv'),
            ('Excel files', '*.xlsx'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Select a data file',
            filetypes=filetypes
        )
        if filename:
            self.file_path.set(filename)
    
    def load_and_plot(self):
        try:
            file_path = self.file_path.get()
            if not file_path:
                raise ValueError("Please select a file first")
            
            # Load data based on file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == '.csv':
                df = pd.read_csv(file_path, sep='\t', index_col=0)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Please use CSV or Excel files.")
            
            # Check required columns
            required_columns = ['Time [s]', 'Minimum [°C]', 'Maximum [°C]', 'Average [°C]']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
            # Get k values
            k_values = self.parse_k_values()
            
            # Plot temperature data
            self.ax_temp.clear()
            self.ax_temp.plot(df['Time [s]'], df['Maximum [°C]'], 'r-', label='Maximum Temperature')
            self.ax_temp.plot(df['Time [s]'], df['Minimum [°C]'], 'b-', label='Minimum Temperature')
            self.ax_temp.plot(df['Time [s]'], df['Average [°C]'], 'g-', label='Average Temperature')
            
            # Customize temperature plot
            self.ax_temp.set_xlabel('Time (s)')
            self.ax_temp.set_ylabel('Temperature (°C)')
            self.ax_temp.set_title('Temperature vs Time')
            self.ax_temp.grid(True)
            self.ax_temp.legend()
            
            # Add temperature statistics
            temp_stats = (
                f"Temperature Statistics:\n"
                f"Max Temp: {df['Maximum [°C]'].max():.1f}°C\n"
                f"Min Temp: {df['Minimum [°C]'].min():.1f}°C\n"
                f"Avg Temp: {df['Average [°C]'].mean():.1f}°C"
            )
            self.ax_temp.text(0.02, 0.98, temp_stats, transform=self.ax_temp.transAxes,
                            verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))
            
            # Plot heat flux data for each k value
            self.ax_flux.clear()
            
            # Create color map for different k values
            colors = plt.cm.rainbow(np.linspace(0, 1, len(k_values)))
            
            max_flux = float('-inf')
            min_flux = float('inf')
            max_transfer = float('-inf')
            
            for k_value, color in zip(k_values, colors):
                heat_flux, heat_transfer_rate = self.calculate_heat_flux(df, k_value)
                self.ax_flux.plot(df['Time [s]'], heat_flux, '-', 
                                color=color, 
                                label=f'k = {k_value} W/m·K')
                
                max_flux = max(max_flux, heat_flux.max())
                min_flux = min(min_flux, heat_flux.min())
                max_transfer = max(max_transfer, heat_transfer_rate.max())
            
            # Customize heat flux plot
            self.ax_flux.set_xlabel('Time (s)')
            self.ax_flux.set_ylabel('Heat Flux (W/m²)')
            self.ax_flux.set_title('Heat Flux vs Time')
            self.ax_flux.grid(True)
            self.ax_flux.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Add heat flux statistics
            flux_stats = (
                f"Heat Flux Statistics:\n"
                f"Max Flux: {max_flux:.1f} W/m²\n"
                f"Min Flux: {min_flux:.1f} W/m²\n"
                f"Max Heat Transfer: {max_transfer:.1f} W"
            )
            self.ax_flux.text(0.02, 0.98, flux_stats, transform=self.ax_flux.transAxes,
                            verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))
            
            # Update both canvases
            self.fig_temp.tight_layout()
            self.fig_flux.tight_layout()
            self.canvas_temp.draw()
            self.canvas_flux.draw()
            
            messagebox.showinfo("Success", "Data loaded and plotted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperaturePlotGUI(root)
    root.mainloop() 