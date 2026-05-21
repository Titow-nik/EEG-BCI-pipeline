# EEG Signal Processing Pipeline for BCI & VR Research

A modular Python pipeline for loading, filtering, and extracting spectral features from EEG data. Built with `MNE-Python`, `SciPy`, and `Pandas`, this project serves as a foundational toolkit for brain-computer interface (BCI) research and immersive VR system development.

## Project Overview
Raw EEG signals are noisy and high-dimensional. This pipeline transforms `.edf` recordings into structured, interpretable features (Theta, Alpha, Beta power) suitable for statistical analysis, machine learning, or real-time BCI applications.

**Key goals:**
- Reproducible preprocessing workflow
- Standardized spectral feature extraction
- Publication-ready visualizations
- Modular architecture for easy extension

## Features

| Module | Description |
|--------|-------------|
| `data_loader.py` | Loads EDF files via MNE, applies standard EEGBCI montage |
| `preprocessing.py` | Bandpass (1–40 Hz) + Notch (50 Hz) filtering, signal visualization |
| `features.py` | Welch PSD estimation, Theta/Alpha/Beta power extraction, CSV & statistics export |
| `main.py` | Orchestrates the full pipeline end-to-end |

## Project Structure
EEG/
├── src/
│ ├── init.py
│ ├── main.py # Pipeline orchestrator
│ ├── data_loader.py # EDF loading & standardization
│ ├── preprocessing.py # Filtering & time-domain visualization
│ └── features.py # Spectral feature extraction & plotting
├── data/
│ └── processed/ # Output CSVs & statistics
├── docs/ # Generated plots & reports
├── requirements.txt # Python dependencies
└── README.md

##  Installation

Requires Python 3.10+

# Clone or download the repository
cd EEG

# Create & activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

## Outputs
| File | Description |
|------|-------------|
| `docs/preprocessing_demo.png` | Raw vs. Filtered EEG (time domain, 0–5s) |
| `docs/features_bar_chart.png` | Theta/Alpha/Beta power distribution (first 8 channels) |
| `data/processed/*_features.csv` | Channel-wise spectral power (µV²) |
| `data/processed/*_statistics.csv` | Mean & Max values across all channels |

## Methodology
Data Loading: MNE-Python reads standard EDF files and applies the EEGBCI 10-20 montage.
Filtering:
Bandpass: 1–40 Hz (removes DC drift & high-frequency noise)
Notch: 50 Hz (eliminates mains interference)
Feature Extraction:
Power Spectral Density (PSD) estimated via Welch's method (2s windows, 50% overlap)
Integrated power calculated for Theta (4–7 Hz), Alpha (8–13 Hz), Beta (14–30 Hz)
Signals converted to microvolts (µV) for interpretable power values
Export: Structured CSV format compatible with Excel, R, or ML frameworks.

## Next Steps
ICA-based artifact removal (eye blinks, muscle noise)
Real-time processing wrapper for live BCI
Machine learning classification (relaxed vs. focused states)
Multi-subject batch processing & statistical testing

Author
Nikita Titow
titow_nik11@mail.ru | https://github.com/Titow-nik
Undergraduate Researcher | Interested in BCI, Neuroengineering & Immersive VR