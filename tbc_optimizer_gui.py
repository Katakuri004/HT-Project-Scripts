import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tbc_optimizer import TBCOptimizer
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import os
from datetime import datetime

class TBCOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TBC Optimizer")
        self.root.geometry("1400x800")
        
        # Create main frames
        self.create_input_frame()
        self.create_notebook()
        self.create_results_frame()
        
        # Initialize optimizer
        self.optimizer = TBCOptimizer()
        
        # Add export button
        self.export_btn = ttk.Button(
            self.root, 
            text="Export Results", 
            command=self.export_results,
            state='disabled'
        )
        self.export_btn.grid(row=2, column=0, pady=5, padx=10, sticky='w')
        
        # Configure auto-update
        self.auto_update = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.root, 
            text="Real-time Plot Updates", 
            variable=self.auto_update
        ).grid(row=2, column=1, pady=5, padx=10, sticky='w')
        
    def create_input_frame(self):
        """Create frame for input parameters"""
        input_frame = ttk.LabelFrame(self.root, text="Input Parameters", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # File selection
        ttk.Label(input_frame, text="Data File:").grid(row=0, column=0, padx=5, pady=5)
        self.file_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5)
        
        # Add data preview button
        ttk.Button(input_frame, text="Preview Data", command=self.preview_data).grid(row=0, column=3, padx=5)
        
        # Optimization parameters
        param_frame = ttk.LabelFrame(input_frame, text="Optimization Parameters", padding="5")
        param_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky="nsew")
        
        # Number of iterations
        ttk.Label(param_frame, text="Number of Iterations:").grid(row=0, column=0, padx=5, pady=5)
        self.n_iterations = tk.StringVar(value="75")
        ttk.Entry(param_frame, textvariable=self.n_iterations, width=10).grid(row=0, column=1, padx=5)
        
        # Update interval
        ttk.Label(param_frame, text="Update Interval (iterations):").grid(row=0, column=2, padx=5, pady=5)
        self.update_interval = tk.StringVar(value="5")
        ttk.Entry(param_frame, textvariable=self.update_interval, width=10).grid(row=0, column=3, padx=5)
        
        # Weights
        weights_frame = ttk.LabelFrame(param_frame, text="Objective Function Weights", padding="5")
        weights_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky="nsew")
        
        self.weights = {}
        row = 0
        for name, default in [
            ("Fatigue Life", 0.4),
            ("Von Mises Stress", -0.3),
            ("Heat Flux Reduction", 0.2),
            ("Cracking Probability", -0.1)
        ]:
            ttk.Label(weights_frame, text=f"{name}:").grid(row=row, column=0, padx=5, pady=2)
            self.weights[name] = tk.StringVar(value=str(default))
            ttk.Entry(weights_frame, textvariable=self.weights[name], width=10).grid(row=row, column=1, padx=5)
            row += 1
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            input_frame, 
            variable=self.progress_var, 
            maximum=100
        )
        self.progress_bar.grid(row=2, column=0, columnspan=4, sticky='ew', pady=5)
        
        # Run button
        self.run_btn = ttk.Button(input_frame, text="Run Optimization", command=self.run_optimization)
        self.run_btn.grid(row=3, column=0, columnspan=4, pady=10)
        
    def create_notebook(self):
        """Create notebook for visualizations"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")
        
        # Create tabs
        self.create_optimization_tab()
        self.create_correlation_tab()
        self.create_surface_tab()
        self.create_parallel_coords_tab()
        
    def create_optimization_tab(self):
        """Create tab for optimization plots"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Optimization Progress")
        
        self.opt_figure = plt.Figure(figsize=(10, 8))
        self.opt_canvas = FigureCanvasTkAgg(self.opt_figure, tab)
        self.opt_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_correlation_tab(self):
        """Create tab for correlation analysis"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Correlation Analysis")
        
        self.corr_figure = plt.Figure(figsize=(10, 8))
        self.corr_canvas = FigureCanvasTkAgg(self.corr_figure, tab)
        self.corr_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_surface_tab(self):
        """Create tab for 3D surface plots"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Response Surface")
        
        self.surface_figure = plt.Figure(figsize=(10, 8))
        self.surface_canvas = FigureCanvasTkAgg(self.surface_figure, tab)
        self.surface_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_parallel_coords_tab(self):
        """Create tab for parallel coordinates plot"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Parallel Coordinates")
        
        self.parallel_figure = plt.Figure(figsize=(10, 8))
        self.parallel_canvas = FigureCanvasTkAgg(self.parallel_figure, tab)
        self.parallel_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_results_frame(self):
        """Create frame for optimization results"""
        results_frame = ttk.LabelFrame(self.root, text="Optimization Results", padding="10")
        results_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Results text
        self.results_text = tk.Text(results_frame, height=10, width=50)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def browse_file(self):
        """Browse for data file"""
        filename = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            
    def preview_data(self):
        """Preview the data file before optimization"""
        try:
            if not self.file_path.get():
                messagebox.showwarning("Warning", "Please select a data file first")
                return
                
            df = pd.read_csv(self.file_path.get())
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Data Preview")
            preview_window.geometry("800x600")
            
            # Add text widget for data display
            text_widget = tk.Text(preview_window, wrap=tk.NONE)
            text_widget.pack(expand=True, fill='both')
            
            # Add scrollbars
            y_scrollbar = ttk.Scrollbar(preview_window, orient='vertical', command=text_widget.yview)
            y_scrollbar.pack(side='right', fill='y')
            x_scrollbar = ttk.Scrollbar(preview_window, orient='horizontal', command=text_widget.xview)
            x_scrollbar.pack(side='bottom', fill='x')
            
            text_widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
            
            # Display data info
            text_widget.insert('end', "Data Summary:\n\n")
            text_widget.insert('end', f"Number of rows: {len(df)}\n")
            text_widget.insert('end', f"Number of columns: {len(df.columns)}\n\n")
            text_widget.insert('end', "Column Info:\n")
            for col in df.columns:
                missing = df[col].isnull().sum()
                text_widget.insert('end', f"{col}:\n")
                text_widget.insert('end', f"  - Missing values: {missing}\n")
                text_widget.insert('end', f"  - Data type: {df[col].dtype}\n")
                if np.issubdtype(df[col].dtype, np.number):
                    text_widget.insert('end', f"  - Range: [{df[col].min()}, {df[col].max()}]\n")
                text_widget.insert('end', "\n")
            
            text_widget.insert('end', "\nFirst 5 rows of data:\n")
            text_widget.insert('end', df.head().to_string())
            
            text_widget.configure(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error previewing data: {str(e)}")
    
    def update_plots(self):
        """Update all plots"""
        if self.auto_update.get():
            self.update_optimization_plot()
            self.update_correlation_plot()
            self.update_surface_plot()
            self.update_parallel_coords_plot()
            self.root.update()
    
    def export_results(self):
        """Export optimization results to files"""
        try:
            # Create results directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = f"optimization_results_{timestamp}"
            os.makedirs(export_dir, exist_ok=True)
            
            # Export optimization parameters and results
            results_dict = {
                "Optimization Parameters": {
                    "Number of Iterations": self.n_iterations.get(),
                    "Weights": {k: v.get() for k, v in self.weights.items()}
                },
                "Best Parameters": {
                    "Thickness": f"{self.best_params[0]:.2f} mm",
                    "Thermal Conductivity": f"{self.best_params[1]:.2f} W/m·K",
                    "Specific Heat Capacity": f"{self.best_params[2]:.2f} J/kg·K",
                    "CTE": f"{self.best_params[3]:.2e} 1/K"
                },
                "Objective Score": f"{self.best_score:.4f}",
                "Optimization History": self.optimizer.optimization_history
            }
            
            # Save results to JSON
            pd.Series(results_dict).to_json(
                os.path.join(export_dir, "optimization_results.json"),
                indent=4
            )
            
            # Save plots
            self.opt_figure.savefig(os.path.join(export_dir, "optimization_progress.png"))
            self.corr_figure.savefig(os.path.join(export_dir, "correlation_analysis.png"))
            self.surface_figure.savefig(os.path.join(export_dir, "response_surface.png"))
            self.parallel_figure.savefig(os.path.join(export_dir, "parallel_coordinates.png"))
            
            # Export optimization data
            optimization_data = pd.DataFrame({
                'Iteration': range(len(self.optimizer.optimization_history)),
                'Best Score': self.optimizer.optimization_history
            })
            optimization_data.to_csv(os.path.join(export_dir, "optimization_history.csv"), index=False)
            
            messagebox.showinfo("Success", f"Results exported to {export_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting results: {str(e)}")
    
    def run_optimization(self):
        """Run the optimization process with real-time updates"""
        try:
            # Disable buttons during optimization
            self.run_btn.configure(state='disabled')
            self.export_btn.configure(state='disabled')
            
            # Update optimizer weights
            self.optimizer.weights = {
                'fatigue_life': float(self.weights["Fatigue Life"].get()),
                'von_mises': float(self.weights["Von Mises Stress"].get()),
                'heat_flux_reduction': float(self.weights["Heat Flux Reduction"].get()),
                'cracking_prob': float(self.weights["Cracking Probability"].get())
            }
            
            # Load data
            df = pd.read_csv(self.file_path.get())
            
            # Check for NaN values
            if df.isna().any().any():
                # Handle NaN values by dropping rows with any NaN
                df = df.dropna()
                if len(df) == 0:
                    raise ValueError("No valid data remains after removing NaN values")
                messagebox.showwarning("Warning", "Some rows containing NaN values were removed from the analysis.")
            
            # Update the data in optimizer
            if not self.optimizer.load_data(df):
                raise ValueError("Failed to load data")
            
            # Get parameters
            n_iterations = int(self.n_iterations.get())
            update_interval = int(self.update_interval.get())
            
            # Run optimization with progress updates
            self.best_params, self.best_score = self.optimizer.optimize(
                n_iterations=n_iterations,
                callback=lambda i: self.update_progress(i, n_iterations, update_interval)
            )
            
            # Update results text
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Optimal TBC Parameters:\n\n")
            self.results_text.insert(tk.END, f"Thickness: {self.best_params[0]:.2f} mm\n")
            self.results_text.insert(tk.END, f"Thermal Conductivity: {self.best_params[1]:.2f} W/m·K\n")
            self.results_text.insert(tk.END, f"Specific Heat Capacity: {self.best_params[2]:.2f} J/kg·K\n")
            self.results_text.insert(tk.END, f"CTE: {self.best_params[3]:.2e} 1/K\n")
            self.results_text.insert(tk.END, f"\nObjective Score: {self.best_score:.4f}")
            
            # Final plot update
            self.update_plots()
            
            # Enable export button
            self.export_btn.configure(state='normal')
            self.run_btn.configure(state='normal')
            
            messagebox.showinfo("Success", "Optimization completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.run_btn.configure(state='normal')
    
    def update_progress(self, iteration, total_iterations, update_interval):
        """Update progress bar and plots"""
        progress = (iteration + 1) / total_iterations * 100
        self.progress_var.set(progress)
        
        if (iteration + 1) % update_interval == 0:
            self.update_plots()
        
        self.root.update()
        
    def update_optimization_plot(self):
        """Update optimization progress plots"""
        self.opt_figure.clear()
        
        # Create subplots similar to the original implementation
        gs = self.opt_figure.add_gridspec(2, 2)
        ax1 = self.opt_figure.add_subplot(gs[0, 0])
        ax2 = self.opt_figure.add_subplot(gs[0, 1])
        ax3 = self.opt_figure.add_subplot(gs[1, 0])
        ax4 = self.opt_figure.add_subplot(gs[1, 1])
        
        # Plot 1: Predicted vs Actual
        y_pred = self.optimizer.gp.predict(self.optimizer.X_train)
        ax1.scatter(self.optimizer.y_train, y_pred, c='blue', alpha=0.5)
        ax1.plot([self.optimizer.y_train.min(), self.optimizer.y_train.max()],
                 [self.optimizer.y_train.min(), self.optimizer.y_train.max()],
                 'r--', lw=2)
        ax1.set_xlabel('Actual Score')
        ax1.set_ylabel('Predicted Score')
        ax1.set_title('Prediction Accuracy')
        
        # Plot 2: Optimization History
        ax2.plot(range(len(self.optimizer.optimization_history)),
                self.optimizer.optimization_history, 'b-', label='Best Score')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Objective Score')
        ax2.set_title('Optimization History')
        ax2.legend()
        
        # Plot 3: Parameter Evolution
        X_unscaled = self.optimizer.scaler_X.inverse_transform(self.optimizer.X_train)
        param_names = list(self.optimizer.bounds.keys())
        for i in range(X_unscaled.shape[1]):
            ax3.plot(range(len(X_unscaled)), X_unscaled[:, i],
                    label=param_names[i], alpha=0.7)
        ax3.set_xlabel('Iteration')
        ax3.set_ylabel('Parameter Value')
        ax3.set_title('Parameter Evolution')
        ax3.legend()
        
        # Plot 4: Uncertainty Evolution
        _, std = self.optimizer.gp.predict(self.optimizer.X_train, return_std=True)
        ax4.plot(range(len(std)), std, 'r-', label='Prediction Uncertainty')
        ax4.set_xlabel('Iteration')
        ax4.set_ylabel('Standard Deviation')
        ax4.set_title('Model Uncertainty')
        ax4.legend()
        
        self.opt_figure.tight_layout()
        self.opt_canvas.draw()
        
    def update_correlation_plot(self):
        """Update correlation analysis plot"""
        self.corr_figure.clear()
        ax = self.corr_figure.add_subplot(111)
        
        # Calculate correlations
        data = pd.DataFrame(self.optimizer.scaler_X.inverse_transform(self.optimizer.X_train),
                           columns=list(self.optimizer.bounds.keys()))
        data['Objective Score'] = self.optimizer.y_train
        
        # Create correlation matrix
        corr = data.corr()
        
        # Plot correlation heatmap
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Parameter Correlation Matrix')
        
        self.corr_figure.tight_layout()
        self.corr_canvas.draw()
        
    def update_surface_plot(self):
        """Update 3D response surface plot"""
        self.surface_figure.clear()
        ax = self.surface_figure.add_subplot(111, projection='3d')
        
        # Create grid for two most important parameters
        param_names = list(self.optimizer.bounds.keys())
        x_param, y_param = param_names[0], param_names[1]  # Using first two parameters
        
        x = np.linspace(self.optimizer.bounds[x_param][0],
                       self.optimizer.bounds[x_param][1], 20)
        y = np.linspace(self.optimizer.bounds[y_param][0],
                       self.optimizer.bounds[y_param][1], 20)
        X, Y = np.meshgrid(x, y)
        
        # Create input points for prediction
        grid_points = np.column_stack((X.ravel(), Y.ravel()))
        other_params = np.median(self.optimizer.X_train[:, 2:], axis=0)
        other_params = np.tile(other_params, (len(grid_points), 1))
        X_pred = np.hstack((grid_points, other_params))
        
        # Get predictions
        Z = self.optimizer.gp.predict(self.optimizer.scaler_X.transform(X_pred))
        Z = Z.reshape(X.shape)
        
        # Plot surface
        surf = ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel(x_param)
        ax.set_ylabel(y_param)
        ax.set_zlabel('Predicted Score')
        ax.set_title('Response Surface')
        
        self.surface_figure.colorbar(surf)
        self.surface_figure.tight_layout()
        self.surface_canvas.draw()
        
    def update_parallel_coords_plot(self):
        """Update parallel coordinates plot"""
        self.parallel_figure.clear()
        ax = self.parallel_figure.add_subplot(111)
        
        # Prepare data
        data = pd.DataFrame(self.optimizer.scaler_X.inverse_transform(self.optimizer.X_train),
                           columns=list(self.optimizer.bounds.keys()))
        data['Objective Score'] = self.optimizer.y_train
        
        # Plot parallel coordinates
        pd.plotting.parallel_coordinates(data, 'Objective Score',
                                      colormap=plt.cm.viridis, ax=ax)
        ax.set_title('Parallel Coordinates Plot')
        
        self.parallel_figure.tight_layout()
        self.parallel_canvas.draw()

def main():
    root = tk.Tk()
    app = TBCOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 