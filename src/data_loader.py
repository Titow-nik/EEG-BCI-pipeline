import mne

def load_eeg_data(subject_id: int = 1):
    file_paths = mne.datasets.eegbci.load_data(subject_id, runs=[6, 10, 14])
    raw = mne.io.read_raw_edf(file_paths[0], preload=True)
    mne.datasets.eegbci.standardize(raw)
    return raw

if __name__ == '__main__':
    print("Initializing data loading...")
    raw_data = load_eeg_data(subject_id=1)

    print(f"Number of channels: {raw_data.info['nchan']}")
    print(f"Sampling frequency: {raw_data.info['sfreq']} Hz")
    print(f"Segment duration: {raw_data.times[-1]:.1f} sec")
    print(f"Object type: {type(raw_data).__name__}")