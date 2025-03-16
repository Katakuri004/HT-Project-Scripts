# 🔥 4-Stroke IC Engine Temperature and Pressure Simulation

![Engine Cycle](https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/4StrokeEngine_Diagram.gif/220px-4StrokeEngine_Diagram.gif)

## 📋 Overview
This sophisticated simulation models the thermodynamic behavior of a four-stroke internal combustion engine, providing detailed temperature and pressure profiles throughout the complete engine cycle. The model incorporates advanced thermodynamic principles and empirical relationships to achieve realistic results.

---

## 🎯 Objective
The project aims to:
- Simulate real-time temperature and pressure variations in a 4-stroke engine
- Model all four strokes: Intake → Compression → Power → Exhaust
- Account for heat transfer and thermodynamic losses
- Generate visualizations for analysis and understanding

---

## 🛠️ Methodology
The simulation employs multiple sophisticated models and principles:

### 1. Slider-Crank Mechanism
```math
V(θ) = V_c [1 + \frac{CR-1}{2}(R + 1 - cos(θ) - \sqrt{R^2 - sin^2(θ)})]
```
Where:
- V(θ): Instantaneous cylinder volume
- V_c: Clearance volume
- CR: Compression ratio
- R: Connecting rod to crank radius ratio
- θ: Crank angle

### 2. Wiebe Function (Combustion Model)
```math
x_b = 1 - exp[-a(\frac{θ - θ_s}{Δθ})^m]
```
- x_b: Mass fraction burned
- a: Efficiency parameter (typically 5)
- m: Shape parameter (typically 2-3)
- θ_s: Start of combustion
- Δθ: Combustion duration

### 3. Heat Transfer Model
```math
Q_{loss} = h_c A (T_{gas} - T_{wall})
```
Where h_c varies with:
- Engine speed
- Gas temperature
- Wall temperature
- Pressure
- Crank angle position

---

## 🌡️ Thermodynamic Concepts

### 1. Polytropic Process
#### Theory
The process follows the relation:
```math
PV^n = constant
```
Where n varies by stroke:
- **Compression**: n ≈ 1.35
  - Higher than adiabatic (γ = 1.4)
  - Lower than isothermal (n = 1.0)
  - Accounts for heat transfer
- **Expansion**: n = 1.25-1.3
  - Variable with temperature
  - Affected by heat losses

#### Implementation
```python
# During compression
temperatures[i] = t_ref * (1/vol_ratio)**(n-1)
pressures[i] = p_ref * (1/vol_ratio)**n
```

### 2. Ideal Gas Law
#### Theory
The fundamental equation:
```math
\frac{P_1V_1}{T_1} = \frac{P_2V_2}{T_2}
```

#### Application
- State changes during compression/expansion
- Pressure calculations during combustion
- Volume-temperature relationships

### 3. Heat Transfer
#### Newton's Law Adaptation
```math
\dot{Q} = h(θ) A(θ) [T_{gas}(θ) - T_{wall}]
```

#### Implementation
```python
def heat_loss_factor(theta, peak_temp, current_temp, ambient_temp):
    base_loss = 0.02  # Base coefficient
    temp_factor = (current_temp - ambient_temp) / (peak_temp - ambient_temp)
    return base_loss * (1 + temp_factor)
```

### 4. Combustion Thermodynamics
#### Key Aspects
- **Heat Release Rate**:
  ```math
  \frac{dQ}{dθ} = Q_{total} \frac{dx_b}{dθ}
  ```
- **Variable Specific Heat Ratio**:
  ```math
  γ = γ_0 - kT
  ```
  Where k is temperature dependency factor

---

## 🔄 Four-Stroke Cycle Implementation

### 1. Intake Stroke (0° - 180°)
![Intake Stroke](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/4-Stroke-Engine-Intake-Stroke.gif/120px-4-Stroke-Engine-Intake-Stroke.gif)

#### Characteristics
- Temperature: Near ambient (≈ 298K)
- Pressure: Slightly below atmospheric
- Volume: Increases from V_min to V_max

#### Code Implementation
```python
# Intake stroke modeling
if theta <= 180:
    temperatures[i] = initial_temp * 0.98
    pressures[i] = initial_pressure * 0.95
```

### 2. Compression Stroke (180° - 360°)
![Compression Stroke](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/4-Stroke-Engine-Compression-Stroke.gif/120px-4-Stroke-Engine-Compression-Stroke.gif)

#### Process
- Polytropic compression
- Temperature rise: ~400K → ~700K
- Pressure increase: ~1 bar → ~20 bar

### 3. Power Stroke (360° - 540°)
![Power Stroke](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/4-Stroke-Engine-Power-Stroke.gif/120px-4-Stroke-Engine-Power-Stroke.gif)

#### Phases
1. **Combustion**:
   - Duration: ~60° crank angle
   - Peak temperature: ~2500K
   - Peak pressure: ~60-70 bar

2. **Expansion**:
   - Polytropic expansion
   - Continuous heat transfer
   - Work extraction

### 4. Exhaust Stroke (540° - 720°)
![Exhaust Stroke](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/4-Stroke-Engine-Exhaust-Stroke.gif/120px-4-Stroke-Engine-Exhaust-Stroke.gif)

#### Two-Phase Model
1. **Blow-down**:
   ```python
   # Blow-down phase
   decay_factor = np.exp(-2 * progress)
   temperatures[i] = temperatures[i-1] * decay_factor + current_target * (1 - decay_factor)
   ```

2. **Displacement**:
   - Gradual temperature decay
   - Pressure approaches ambient
   - Final cleanup of combustion products

---

## 📊 Results and Visualization

### Temperature Profile
```
     ^
2500 |     ____
  T  |    /    \
 [K] |   /      \
     |  /        \____
 300 |_/              \___
     +-------------------->
     0°      360°     720°
```

### Pressure Profile
```
     ^
 70  |     /\
  P  |    /  \
[bar]|   /    \
     |  /      \____
  1  |_/            \___
     +-------------------->
     0°      360°     720°
```

---

## 🔧 Usage

### Prerequisites
- Python 3.7+
- NumPy
- Matplotlib
- SciPy

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/engine-simulation.git

# Install dependencies
pip install -r requirements.txt
```

### Running the Simulation
```bash
python visualization.py
```

---

## ⚠️ Limitations and Assumptions

### Physical Simplifications
1. **Ideal Gas Behavior**
   - Perfect gas law applies
   - No real gas effects
   - Constant specific heats

2. **Heat Transfer**
   - Simplified convection model
   - No radiation effects
   - Uniform wall temperature

### Model Limitations
1. **Flow Dynamics**
   - No valve flow modeling
   - No pressure wave effects
   - No turbulence modeling

2. **Mechanical Aspects**
   - No friction losses
   - Constant engine speed
   - No mechanical deformation

---

## 📚 References

### Primary Sources
1. Heywood, J.B., "Internal Combustion Engine Fundamentals"
   - Comprehensive engine theory
   - Empirical correlations
   - Performance analysis

2. Ferguson, C.R., "Internal Combustion Engines: Applied Thermosciences"
   - Thermodynamic analysis
   - Combustion modeling
   - Heat transfer correlations

3. Turns, S.R., "An Introduction to Combustion: Concepts and Applications"
   - Combustion theory
   - Chemical kinetics
   - Emission formation

### Additional Resources
- SAE Technical Papers
- Engine simulation journals
- Thermodynamics textbooks

---

## 👥 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

*Note: The GIF images used in this README are for illustration purposes and are sourced from Wikipedia under Creative Commons license.* 