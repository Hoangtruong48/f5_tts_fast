import os
import json
import argparse
from datasets import Dataset
import pandas as pd
import torchaudio


def prepare_dataset(metadata_csv, wav_dir, output_base, dataset_name, tokenizer_type="char"):
    # Tạo đường dẫn thư mục output
    out_dir = os.path.join(output_base, f"{dataset_name}_{tokenizer_type}")
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # Load metadata.csv (wav|text)
    df = pd.read_csv(
        metadata_csv,
        sep="|",
        header=None,
        names=["audio_path", "text"]
    )

    # Chuẩn hóa đường dẫn audio + tính duration
    def process_row(rel_path):
        path = os.path.join(wav_dir, os.path.basename(rel_path))
        if not os.path.exists(path):
            raise FileNotFoundError(f"Không tìm thấy file audio: {path}")
        info = torchaudio.info(path)
        duration_sec = info.num_frames / info.sample_rate
        return path, duration_sec

    audio_paths = []
    durations = []
    for p in df["audio_path"]:
        abs_path, dur = process_row(p)
        audio_paths.append(abs_path)
        durations.append(dur)

    df["audio_path"] = audio_paths
    df["duration"] = durations  # ✅ thêm duration vào dataframe

    # HuggingFace Dataset
    ds = Dataset.from_pandas(df)

    # Save dataset
    ds.save_to_disk(raw_dir)

    # Tạo duration.json
    with open(os.path.join(out_dir, "duration.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": durations}, f, ensure_ascii=False, indent=2)

    # Tạo vocab.txt (char-level)
    all_text = "\n".join(df["text"].astype(str).tolist())
    chars = sorted(set(all_text))
    with open(os.path.join(out_dir, "vocab.txt"), "w", encoding="utf-8") as f:
        for c in chars:
            f.write(c + "\n")

    print(f"✅ Prepared dataset at {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare dataset: raw.arrow, duration.json, vocab.txt")
    parser.add_argument("--metadata_csv", type=str, required=True)
    parser.add_argument("--wav_dir", type=str, required=True)
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--dataset_name", type=str, required=True)
    parser.add_argument("--tokenizer", type=str, default="char")

    args = parser.parse_args()
    prepare_dataset(
        metadata_csv=args.metadata_csv,
        wav_dir=args.wav_dir,
        output_base=args.data_dir,
        dataset_name=args.dataset_name,
        tokenizer_type=args.tokenizer
    )
