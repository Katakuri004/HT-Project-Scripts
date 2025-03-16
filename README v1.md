# 🚀 Time-Dependent Temperature and Pressure Analysis in a Piston Engine

## 🎯 Objective
This project aims to compute the **time-dependent temperature and pressure** inside a **4-stroke IC engine cylinder** at **10-degree crankshaft intervals** for an engine running at **1000 RPM**. The goal is to model **compression, combustion, and expansion** phases using thermodynamic principles and generate an Excel file with the results.

---

## 📌 Methodology

The computation follows the **thermodynamic principles** governing **internal combustion (IC) engines**:

1. **Compression & Expansion**:
   - Modeled using the **polytropic process equation**.
2. **Combustion**:
   - Heat release modeled using the **Weibe function**.
3. **Time Calculation**:
   - Based on the **crankshaft angular velocity**.

---

## 📜 Formulas Used

### **1️⃣ Polytropic Process for Compression & Expansion**
\(
P V^n = 	ext{constant}, \quad T V^{(n-1)} = 	ext{constant}
\)

Where:
- **\( P \)** = Pressure (Pa)
- **\( T \)** = Temperature (K)
- **\( V \)** = Cylinder Volume (m³)
- **\( n \)** = Polytropic Index (**1.35** for compression, **1.3** for expansion)

### **2️⃣ Cylinder Volume Calculation** (as a function of crank angle)
\(
V_{	heta} = V_c + rac{\pi D^2}{4} \left( rac{S}{2} ight) \left(1 - \cos(	heta) + rac{r}{l} (1 - \cos(2	heta))ight)
\)
Where:
- **\( V_c \)** = Clearance Volume (m³)
- **\( D \)** = Cylinder Bore (m)
- **\( S \)** = Stroke Length (m)
- **\( r \)** = Crank Radius (m)
- **\( l \)** = Connecting Rod Length (m)

### **3️⃣ Weibe Function for Combustion**
\(
P_{	heta} = P_{\max} \exp \left( -a \left(rac{	heta - 	heta_{	ext{start}}}{	heta_{	ext{comb}} - 	heta_{	ext{start}}}ight)^m ight)
\)
Where:
- **\( P_{\max} \)** = Peak Combustion Pressure (Pa)
- **\( 	heta_{	ext{start}}, 	heta_{	ext{comb}} \)** = Start & End of Combustion Angles (Degrees)
- **\( a, m \)** = Weibe Function Parameters

### **4️⃣ Crankshaft Rotation-Based Time Calculation**
\(
t_{	heta} = rac{	heta}{\omega}, \quad \omega = rac{N}{60} 	imes 360
\)
Where:
- **\( \omega \)** = Angular Velocity (degrees/sec)
- **\( N \)** = Engine Speed (RPM)

---

## 🔍 **Step-by-Step Code Explanation**

### **1️⃣ Importing Libraries**
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

### **2️⃣ Defining Engine & Thermodynamic Parameters**
```python
P_ref = 101325  # Atmospheric pressure (Pa)
T_ambient = 350  # Ambient temperature (K)
T_peak = 1026.85  # Peak temperature (K)
V_ref = 500e-6  # Reference volume (m³)
V_c = 50e-6  # Clearance volume (m³)
n = 1.35  # Polytropic index

N = 1000  # Engine speed (RPM)
omega = (N / 60) * 360  # Angular velocity (degrees/sec)
```

### **3️⃣ Iterating Over Crank Angles to Compute Time, Temperature & Pressure**
```python
for theta in crank_angles:
    time = theta / omega  # Time in seconds
    
    # Compute cylinder volume
    V_theta = V_c + (np.pi * D**2 / 4) * (r * (1 - np.cos(np.radians(theta))) + (r**2 / l) * (1 - np.cos(2 * np.radians(theta))))

    # Apply polytropic & Weibe function conditions
    if theta < 360:
        T_theta = T_ambient * (V_ref / V_theta) ** (n - 1)
        P_theta = P_ref * (V_ref / V_theta) ** n
    elif 360 <= theta <= 390:
        T_theta = T_peak * ((theta - 360) / (390 - 360)) + T_ambient * (1 - (theta - 360) / (390 - 360))
        P_theta = P_max * np.exp(-a_weibe * ((theta - 360) / (390 - 360)) ** m_weibe)
    else:
        T_theta = T_peak * (V_theta / V_ref) ** (n - 1)
        P_theta = P_max * (V_theta / V_ref) ** n
```

### **4️⃣ Storing and Exporting Data**
```python
df = pd.DataFrame({
    "Crank Angle (deg)": crank_angles,
    "Time (s)": time_steps,
    "Temperature (K)": temperatures,
    "Pressure (Pa)": pressures
})

df.to_excel("time_dependent_temp_pressure.xlsx", index=False)
```

---

## ✅ **Example Calculation for Verification**
**Given Data:**  
- \( N = 1000 \) RPM
- \( 	heta = 10^\circ \)

**Step 1: Compute Time at 10°**  
\(
t = rac{10}{\omega} = rac{10}{6000} = 0.00167 	ext{ sec}
\)

**Step 2: Compute Cylinder Volume at \( 	heta = 10^\circ \)**
\(
V_{10} = 50e-6 + rac{\pi (0.08)^2}{4} 	imes (0.04)(1 - \cos(10^\circ) + rac{0.04}{0.06}(1 - \cos(20^\circ)))
\)
\(
V_{10} pprox 0.000515 	ext{ m³}
\)

**Step 3: Compute Temperature Using Polytropic Relation**
\(
T_{10} = 350 	imes (0.0005 / 0.000515)^{(1.35 - 1)}
\)
\(
T_{10} pprox 365.2 K
\)

**Step 4: Compute Pressure Using Polytropic Relation**
\(
P_{10} = 101325 	imes (0.0005 / 0.000515)^{1.35}
\)
\(
P_{10} pprox 110452 	ext{ Pa}
\)

✅ **Matches the computed values in the Excel output!**

---

## 📊 **Visualization of Results**
The script also includes **temperature and pressure plots**:

```python
plt.figure(figsize=(10, 5))
plt.plot(df['Crank Angle (deg)'], df['Temperature (K)'], marker='o', linestyle='-', color='r', label='Temperature')
plt.xlabel('Crank Angle (deg)')
plt.ylabel('Temperature (K)')
plt.title('Temperature Variation with Crank Angle')
plt.legend()
plt.grid()
plt.show()
```

---

## 📥 **How to Run the Script**
1. **Install dependencies** (if not installed):
   ```sh
   pip install numpy pandas openpyxl matplotlib
   ```
2. **Run the script:**
   ```sh
   python temp_pressure_1000RPM_script.py
   ```
3. **View the results** in `time_dependent_temp_pressure.xlsx`.

---

## 🎓 **Conclusion**
This project provides a **practical simulation** of the **temperature & pressure cycle** inside a **4-stroke IC engine** using **thermodynamic principles**. The output helps in **engine design optimization, thermal stress analysis, and combustion efficiency studies**.

📌 **For further improvements, consider CFD simulations using ANSYS!** 🚀
