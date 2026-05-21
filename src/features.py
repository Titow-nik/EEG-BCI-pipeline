import numpy as np
import mne
import pandas as pd
from pathlib import Path
from scipy.signal import welch
import matplotlib.pyplot as plt


def extract_eeg_features(edf_path, csv_path):

    print(f"Loading file: {edf_path.name}")

    raw = mne.io.read_raw_edf(str(edf_path), preload=True, verbose=False)
    raw.filter(l_freq=1.0, h_freq=40.0, verbose=False)
    raw.notch_filter(freqs=50.0, verbose=False)

    data = raw.get_data() * 1e6
    ch_names = raw.ch_names
    fs = raw.info['sfreq']

    bands = {
        'Theta': (4, 7),
        'Alpha': (8, 13),
        'Beta': (14, 30)
    }

    features_list = []
    nperseg = int(fs * 2)

    for i, ch_data in enumerate(data):
        freqs, psd = welch(ch_data, fs=fs, nperseg=nperseg, scaling='density')

        row = {'Channel': ch_names[i]}
        for band_name, (fmin, fmax) in bands.items():
            mask = (freqs >= fmin) & (freqs <= fmax)
            band_power = np.trapezoid(psd[mask], freqs[mask])
            row[f'{band_name}_Power'] = band_power

        features_list.append(row)

    df = pd.DataFrame(features_list)
    df.to_csv(csv_path, index=False, sep=';', float_format='%.2f', encoding='utf-8-sig')

    print(f"Features extracted and saved: {csv_path}")
    print(f"Table size: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def plot_features_bar(df, save_path):

    df_sample = df.head(8)

    x = np.arange(len(df_sample['Channel']))  # positions for channels
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 6))

    bars1 = ax.bar(x - width, df_sample['Theta_Power'], width, label='Theta (4-7 Hz)', color='#4C72B0')
    bars2 = ax.bar(x, df_sample['Alpha_Power'], width, label='Alpha (8-13 Hz)', color='#55A868')
    bars3 = ax.bar(x + width, df_sample['Beta_Power'], width, label='Beta (14-30 Hz)', color='#C44E52')

    ax.set_xlabel('EEG Channel', fontsize=12)
    ax.set_ylabel('Power (µV²)', fontsize=12)
    ax.set_title('Brain Rhythm Power Distribution (First 8 Channels)', fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(df_sample['Channel'], rotation=45)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Chart saved: {save_path}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    processed_dir = project_root / "data" / "processed"
    docs_dir = project_root / "docs"
    processed_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    edf_matches = list(Path.home().glob("mne_data/**/S001R06.edf"))
    if not edf_matches:
        print("File S001R06.edf not found.")
    else:
        edf_file = edf_matches[0]
        csv_file = processed_dir / "S001R06_features.csv"

        df = extract_eeg_features(edf_file, csv_file)

        plot_features_bar(df, docs_dir / "features_bar_chart.png")

        stats = {
            'Theta_Mean': df['Theta_Power'].mean(),
            'Theta_Max': df['Theta_Power'].max(),
            'Alpha_Mean': df['Alpha_Power'].mean(),
            'Alpha_Max': df['Alpha_Power'].max(),
            'Beta_Mean': df['Beta_Power'].mean(),
            'Beta_Max': df['Beta_Power'].max()
        }

        stats_file = processed_dir / "S001R06_statistics.csv"
        pd.DataFrame([stats]).to_csv(stats_file, index=False, sep=';', float_format='%.2f', encoding='utf-8-sig')
        print(f"Summary statistics saved: {stats_file}")
        print(f"Average Alpha: {stats['Alpha_Mean']:.2f}, Average Beta: {stats['Beta_Mean']:.2f}")