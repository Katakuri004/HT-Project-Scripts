import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import norm
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

class TBCOptimizer:
    def __init__(self):
        self.bounds = {
            'Thickness': (0.1, 2.0),
            'Thermal_Conductivity': (1.0, 4.0),
            'Specific_Heat_Capacity': (500, 1000),
            'CTE': (5e-6, 12e-6)
        }
        self.weights = {
            'fatigue_life': 0.4,
            'von_mises': -0.3,
            'heat_flux_reduction': 0.2,
            'cracking_prob': -0.1
        }
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.optimization_history = []
        
    def load_data(self, data):
        """Load and preprocess training data"""
        try:
            # Extract features (TBC parameters) and targets (performance metrics)
            X_columns = ['Thickness', 'Thermal_Conductivity', 'Specific_Heat_Capacity', 'CTE']
            y_columns = ['Fatigue_Life', 'Von_Mises_Stress', 'Heat_Flux_Reduction', 'Cracking_Probability']
            
            self.X_train = data[X_columns].values
            y_metrics = data[y_columns].values
            
            # Scale the features
            self.X_train = self.scaler_X.fit_transform(self.X_train)
            
            # Calculate weighted objective function
            self.y_train = np.zeros(len(data))
            for i, (metric, weight) in enumerate([
                ('Fatigue_Life', self.weights['fatigue_life']),
                ('Von_Mises_Stress', self.weights['von_mises']),
                ('Heat_Flux_Reduction', self.weights['heat_flux_reduction']),
                ('Cracking_Probability', self.weights['cracking_prob'])
            ]):
                normalized_metric = (data[metric] - data[metric].min()) / (data[metric].max() - data[metric].min())
                self.y_train += weight * normalized_metric
            
            # Initialize Gaussian Process model
            kernel = C(1.0) * RBF([1.0] * self.X_train.shape[1])
            self.gp = GaussianProcessRegressor(
                kernel=kernel,
                n_restarts_optimizer=10,
                random_state=42
            )
            
            # Fit the GP model
            self.gp.fit(self.X_train, self.y_train)
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def optimize(self, n_iterations=100, callback=None):
        """Run Bayesian optimization"""
        best_score = float('-inf')
        best_params = None
        
        for i in range(n_iterations):
            # Sample random points
            X_random = np.random.uniform(
                low=[self.bounds[k][0] for k in self.bounds],
                high=[self.bounds[k][1] for k in self.bounds],
                size=(100, len(self.bounds))
            )
            
            # Scale the random points
            X_random_scaled = self.scaler_X.transform(X_random)
            
            # Get predictions and uncertainties
            y_pred, std = self.gp.predict(X_random_scaled, return_std=True)
            
            # Calculate acquisition function (Upper Confidence Bound)
            acquisition = y_pred + 1.96 * std
            
            # Select best point
            best_idx = np.argmax(acquisition)
            X_new = X_random[best_idx]
            
            # Update training data
            X_new_scaled = self.scaler_X.transform(X_new.reshape(1, -1))
            y_new = self._evaluate_objective(X_new)
            
            self.X_train = np.vstack([self.X_train, X_new_scaled])
            self.y_train = np.append(self.y_train, y_new)
            
            # Update GP model
            self.gp.fit(self.X_train, self.y_train)
            
            # Update best parameters
            if y_new > best_score:
                best_score = y_new
                best_params = X_new
            
            self.optimization_history.append(best_score)
            
            if callback:
                callback(i)
        
        return best_params, best_score
    
    def _evaluate_objective(self, params):
        """Evaluate the objective function for new parameters"""
        # This is a simplified evaluation using the GP model
        # In a real application, this might involve running simulations or experiments
        X_scaled = self.scaler_X.transform(params.reshape(1, -1))
        return float(self.gp.predict(X_scaled))

    def preprocess_data(self, df):
        """Preprocess the data by handling missing values and outliers"""
        # Make a copy to avoid modifying the original data
        df = df.copy()
        
        # Handle missing values
        for column in df.columns:
            if df[column].isnull().any():
                # For numeric columns, use median
                if np.issubdtype(df[column].dtype, np.number):
                    df[column].fillna(df[column].median(), inplace=True)
                else:
                    # For non-numeric columns, use mode
                    df[column].fillna(df[column].mode()[0], inplace=True)
        
        # Handle infinite values
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(df.mean(), inplace=True)
        
        # Remove outliers using IQR method
        for column in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[column] = df[column].clip(lower_bound, upper_bound)
        
        return df

    def plot_optimization_results(self):
        """Enhanced plot of optimization results"""
        fig = plt.figure(figsize=(15, 10))
        
        # Plot 1: Predicted vs Actual
        ax1 = plt.subplot(221)
        y_pred = self.gp.predict(self.X_train)
        ax1.scatter(self.y_train, y_pred, c='blue', alpha=0.5)
        ax1.plot([self.y_train.min(), self.y_train.max()], 
                 [self.y_train.min(), self.y_train.max()], 
                 'r--', lw=2)
        ax1.set_xlabel('Actual Score')
        ax1.set_ylabel('Predicted Score')
        ax1.set_title('Prediction Accuracy')
        
        # Plot 2: Optimization History
        ax2 = plt.subplot(222)
        ax2.plot(range(len(self.optimization_history)), 
                self.optimization_history, 'b-', label='Best Score')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Objective Score')
        ax2.set_title('Optimization History')
        ax2.legend()
        
        # Plot 3: Parameter Evolution
        ax3 = plt.subplot(223)
        X_unscaled = self.scaler_X.inverse_transform(self.X_train)
        param_names = list(self.bounds.keys())
        for i in range(X_unscaled.shape[1]):
            ax3.plot(range(len(X_unscaled)), X_unscaled[:, i], 
                    label=param_names[i], alpha=0.7)
        ax3.set_xlabel('Iteration')
        ax3.set_ylabel('Parameter Value')
        ax3.set_title('Parameter Evolution')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Plot 4: Uncertainty Evolution
        ax4 = plt.subplot(224)
        _, std = self.gp.predict(self.X_train, return_std=True)
        ax4.plot(range(len(std)), std, 'r-', label='Prediction Uncertainty')
        ax4.set_xlabel('Iteration')
        ax4.set_ylabel('Standard Deviation')
        ax4.set_title('Model Uncertainty')
        ax4.legend()
        
        plt.tight_layout()
        return fig

def main():
    # Example usage
    optimizer = TBCOptimizer()
    
    # Load sample data
    if optimizer.load_data('TBC_data.csv'):
        # Run optimization with increased iterations
        best_params, best_score = optimizer.optimize(n_iterations=75)
        
        # Print results
        print("\nOptimal TBC Parameters:")
        print(f"Thickness: {best_params[0]:.2f} mm")
        print(f"Thermal Conductivity: {best_params[1]:.2f} W/m·K")
        print(f"Specific Heat Capacity: {best_params[2]:.2f} J/kg·K")
        print(f"CTE: {best_params[3]:.2e} 1/K")
        print(f"\nObjective Score: {best_score:.4f}")
        
        # Plot results
        fig = optimizer.plot_optimization_results()
        plt.show()

if __name__ == "__main__":
    main() 