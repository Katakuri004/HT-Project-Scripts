# 🔥 Weibe Function for Temperature and Pressure Calculation in IC Engines

## 🎯 Objective
This document explains how to use the **Weibe function** to determine the **time-dependent temperature and pressure** in an **internal combustion (IC) engine** during the **combustion phase**.

---

## 📌 Weibe Function Overview
The **Weibe function** models the **fuel burn fraction** during combustion:

\(
x_b(	heta) = 1 - \exp \left[ -a \left(rac{	heta - 	heta_{	ext{start}}}{	heta_{	ext{comb}} - 	heta_{	ext{start}}}
ight)^m 
ight]
\)

Where:
- **\( x_b(	heta) \)** = Fraction of fuel burned at crank angle \( 	heta \)
- **\( a \)** = Empirical constant (typically **5 to 6** for SI engines)
- **\( m \)** = Shape factor (typically **2 to 3** for SI engines)
- **\( 	heta \)** = Crank angle (in degrees)
- **\( 	heta_{	ext{start}} \)** = Start of combustion (degrees)
- **\( 	heta_{	ext{comb}} \)** = End of combustion (degrees)

---

## 📜 Step-by-Step Calculation

### **1️⃣ Compute Fuel Burned Fraction Using Weibe Function**
For **any crank angle \( 	heta \)** between \( 360^\circ \) and \( 390^\circ \):

\(
x_b(	heta) = 1 - \exp \left[ -5 \left(rac{	heta - 360}{390 - 360}
ight)^2 
ight]
\)

✅ **Example at \( 	heta = 375^\circ \):**  
\( x_b(375) pprox 0.7135 \) (71.35% fuel burned).

---

### **2️⃣ Compute Pressure Using Weibe Function**
\(
P_{	heta} = P_{	ext{max}} \cdot x_b(	heta)
\)
- If **\( P_{	ext{max}} = 3.5 \) MPa**, then:
\(
P_{375} = 3.5 	imes 10^6 	imes 0.7135 = 2.497 	ext{ MPa}
\)

✅ **At \( 375^\circ \), Pressure ≈ 2.497 MPa.**

---

### **3️⃣ Compute Temperature Using Weibe Function**
\(
T_{	heta} = T_{	ext{max}} \cdot x_b(	heta) + T_{	ext{amb}} \cdot (1 - x_b(	heta))
\)
- If **\( T_{	ext{max}} = 1026.85 \) K** and **\( T_{	ext{amb}} = 350 \) K**:
\(
T_{375} pprox 833.23 	ext{ K}
\)

✅ **At \( 375^\circ \), Temperature ≈ 833.23 K.**

---

## **📊 Python Code to Compute Pressure & Temperature at Any Crank Angle**
```python
import numpy as np

# Given data
theta_start = 360  # Start of combustion (degrees)
theta_comb = 390  # End of combustion (degrees)
P_max = 3.5e6  # Peak pressure in Pa
T_max = 1026.85  # Peak temperature in K
T_ambient = 350  # Ambient temperature in K
a = 5  # Weibe function constant
m = 2  # Shape parameter

# Function to compute Weibe function
def weibe_function(theta, theta_start, theta_comb, a, m):
    if theta < theta_start:
        return 0
    elif theta > theta_comb:
        return 1
    else:
        return 1 - np.exp(-a * ((theta - theta_start) / (theta_comb - theta_start)) ** m)

# Function to compute pressure and temperature
def compute_temp_pressure(theta):
    xb = weibe_function(theta, theta_start, theta_comb, a, m)
    P_theta = P_max * xb
    T_theta = T_max * xb + T_ambient * (1 - xb)
    return P_theta, T_theta

# Example computation for theta = 375°
theta_test = 375
P_test, T_test = compute_temp_pressure(theta_test)

print(f"At {theta_test}°:")
print(f"Pressure = {P_test:.2f} Pa")
print(f"Temperature = {T_test:.2f} K")
```

---

## **📊 Conclusion**
✅ **The Weibe function** accurately models the **combustion phase** in an IC engine.  
✅ It helps in **determining pressure and temperature** at **any crank angle**.  
✅ Used extensively in **engine simulations (MATLAB, ANSYS, GT-Power, Python, etc.)**.

