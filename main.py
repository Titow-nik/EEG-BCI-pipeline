import sys
from pathlib import Path

# Автоматически добавляем папку src/ в пути поиска Python
script_dir = Path(__file__).parent
src_dir = script_dir / "src" if (script_dir / "src").is_dir() else script_dir
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from data_loader import load_eeg_data
from preprocessing import run_preprocessing
from features import extract_eeg_features


def main():
    print("Starting EEG Processing Pipeline\n")

    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data" / "processed"
    docs_dir = project_root / "docs"
    data_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load
    print("STEP 1: Loading Data")
    raw_path = Path.home() / "mne_data" / "MNE-eegbci-data" / "files" / "eegmmidb" / "1.0.0" / "S001" / "S001R06.edf"
    if not raw_path.exists():
        print("Data file not found. Please download first.")
        return
    print(f"Data loaded: {raw_path.name}\n")

    # 2. Preprocess
    print("STEP 2: Preprocessing")
    run_preprocessing()
    print()

    # 3. Extract Features
    print("STEP 3: Feature Extraction")
    csv_path = data_dir / "S001R06_features.csv"
    extract_eeg_features(raw_path, csv_path)
    print()

    print("Pipeline completed successfully!")
    print(f"Outputs:")
    print(f"   - {docs_dir / 'preprocessing_demo.png'}")
    print(f"   - {docs_dir / 'features_bar_chart.png'}")
    print(f"   - {data_dir / 'S001R06_features.csv'}")
    print(f"   - {data_dir / 'S001R06_statistics.csv'}")


if __name__ == "__main__":
    main()
