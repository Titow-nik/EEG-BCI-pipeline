import numpy as np
import mne
import matplotlib.pyplot as plt
from pathlib import Path

def run_preprocessing():
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    raw_path = Path.home() / "mne_data" / "MNE-eegbci-data" / "files" / "eegmmidb" / "1.0.0" / "S001" / "S001R06.edf"

    if not raw_path.exists():
        print("Error: Data file not found.")
        print(f"Expected path: {raw_path}")
        print("Download data using: mne.datasets.eegbci.load_data([1], [6])")
        return

    print("Loading raw data...")
    raw = mne.io.read_raw_edf(str(raw_path), preload=True, verbose=False)

    print("Applying filtering...")
    raw_filt = raw.copy()
    raw_filt.filter(l_freq=1.0, h_freq=40.0, verbose=False)
    raw_filt.notch_filter(freqs=50.0, verbose=False)
    print("Filtering complete: 1.0-40.0 Hz, 50.0 Hz notch removed")

    print(f"Original signal shape: {raw.get_data().shape}")
    print(f"Filtered signal shape: {raw_filt.get_data().shape}")

    print("Generating plot...")
    picks = mne.pick_types(raw.info, meg=False, eeg=True)[:3]
    if len(picks) == 0:
        picks = list(range(min(3, raw.n_channels)))

    t_start, t_stop = 0.0, 5.0
    idx_start, idx_stop = raw.time_as_index([t_start, t_stop])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
    times = raw.times[idx_start:idx_stop]
    scale = 1e6

    data_raw = raw.get_data(picks=picks, start=idx_start, stop=idx_stop) * scale
    for i, ch_data in enumerate(data_raw):
        ax1.plot(times, ch_data + i * 200, label=raw.ch_names[picks[i]])
    ax1.set_title("Raw Signal (0-5 sec)")
    ax1.set_ylabel("Amplitude (µV)")
    ax1.legend(loc='upper right')

    data_filt = raw_filt.get_data(picks=picks, start=idx_start, stop=idx_stop) * scale
    for i, ch_data in enumerate(data_filt):
        ax2.plot(times, ch_data + i * 200, label=raw.ch_names[picks[i]])
    ax2.set_title("Filtered Signal (1-40 Hz, notch 50 Hz)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Amplitude (µV)")

    plt.tight_layout()
    save_path = docs_dir / "preprocessing_demo.png"
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Filtering complete, plot saved: {save_path}")

if __name__ == "__main__":
    run_preprocessing()