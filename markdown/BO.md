# 🔥 Bayesian Optimization for Thermal Barrier Coating (TBC) Optimization 🚀

## 📌 Overview
This repository contains an **implementation of Bayesian Optimization** for optimizing **Thermal Barrier Coating (TBC) parameters** used in **Otto cycle four-stroke petrol engine pistons**.  
The goal is to **maximize fatigue life** while **minimizing thermal stress and cracking probability** by selecting the best **TBC thickness, material, and thermal properties**.

---

## 🎯 **Objective**
- ✅ Find the **optimal TBC thickness** for maximum durability.
- ✅ Reduce **thermal fatigue failure** by selecting **optimal material properties**.
- ✅ Minimize **Von Mises stress** and **thermal expansion mismatch**.
- ✅ Maximize **heat flux reduction** for better insulation.
- ✅ Optimize coating parameters **faster than traditional simulations**.

---

## ⚡ **Concepts Involved**
### **1️⃣ Bayesian Optimization**
Bayesian Optimization is an **intelligent search algorithm** that finds the **best set of parameters** without exhaustive testing. It:
- Learns from **previous evaluations** to **predict** better parameter combinations.
- Uses a **Gaussian Process (GP) Regression model** to estimate unknown values.
- Chooses **promising parameter sets** for evaluation.
- **Reduces computational cost** in simulations by optimizing parameter selection.

🔹 **Formula Used for Optimization (Objective Function):**
\[
Score = \alpha (N_f) - \beta (\sigma_{vonMises}) + \gamma (Heat Flux Reduction) - \delta (Cracking Probability)
\]
where:
- \( N_f \) = Fatigue Life (Higher is better ✅)
- \( \sigma_{vonMises} \) = Von Mises Stress (Lower is better ✅)
- **Heat Flux Reduction (%)** = Higher is better ✅
- **Cracking Probability (%)** = Lower is better ✅

---

## 📥 **Dataset Structure**
The dataset (`TBC_data.csv`) contains **thermal and mechanical performance metrics** of different **coating materials and thicknesses**.

### **🔹 Features (Inputs)**
| Feature Name                 | Unit      | Description |
|------------------------------|----------|-------------|
| **TBC Thickness**            | mm       | Coating thickness |
| **Thermal Conductivity (k)**  | W/m·K    | Heat insulation property |
| **Specific Heat Capacity (Cp)** | J/kg·K | Heat absorption |
| **Coefficient of Thermal Expansion (CTE)** | 1/K | Expansion mismatch with substrate |

### **🔹 Performance Metrics (Outputs)**
| Feature Name                 | Unit    | Goal |
|------------------------------|--------|------|
| **Max Temperature (T_max)**   | K      | 🔻 Lower is better |
| **Heat Flux Reduction (%)**   | %      | 🔺 Higher is better |
| **Thermal Fatigue Life (N_f)** | Cycles | 🔺 Higher is better |
| **Von Mises Stress (σ_vm)**   | MPa    | 🔻 Lower is better |
| **Cracking Probability**      | %      | 🔻 Lower is better |

---

