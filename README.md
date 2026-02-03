# Osdag Screening Task  
## Visualization of Shear Force and Bending Moment Diagrams using Xarray and Plotly

This repository contains the complete implementation of the Osdag screening task
focused on post-processing and visualization of **Shear Force Diagrams (SFD)**
and **Bending Moment Diagrams (BMD)** for a bridge grillage model.

The project demonstrates how internal force data stored in an **Xarray dataset**
can be effectively extracted, processed, and visualized using **interactive 2D
and 3D plots**, similar to commercial structural analysis software such as MIDAS.

---

## 🔍 Project Overview

In bridge grillage analysis, large volumes of internal force data are generated
for multiple structural members. Effective visualization of these results is
essential for engineering interpretation and design validation.

This project addresses that requirement by:
- Generating continuous **2D SFD and BMD** for a central longitudinal girder
- Creating **3D MIDAS-style SFD and BMD visualizations** for all longitudinal girders
- Preserving original dataset sign conventions and force magnitudes

The work aligns with the Osdag and FOSSEE objective of promoting open-source
structural engineering tools and workflows.

---

## 🎯 Objectives

- Extract shear force (Vy) and bending moment (Mz) values from an Xarray dataset
- Plot continuous 2D SFD and BMD for the central longitudinal girder
- Generate 3D force visualizations for all girders using actual bridge geometry
- Present results in a clear, interpretable, and engineering-oriented manner
