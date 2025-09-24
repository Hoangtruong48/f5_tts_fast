import argparse
import torch
from safetensors.torch import save_file


def convert_pt_to_safetensors(input_path: str, output_path: str):
    print(f"Đang load checkpoint từ {input_path} ...")
    checkpoint = torch.load(input_path, map_location="cpu")

    # Nếu file .pt chứa "model_state_dict" thì lấy nó ra,
    # còn nếu chỉ là state_dict thì dùng trực tiếp
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
    else:
        state_dict = checkpoint

    print(f" Đang lưu sang {output_path} ...")
    save_file(state_dict, output_path)
    print("✅ Convert thành công!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PyTorch .pt checkpoint to .safetensors format")
    parser.add_argument("input", type=str, help="Đường dẫn file .pt")
    parser.add_argument("output", type=str, help="Đường dẫn file .safetensors (output)")

    args = parser.parse_args()
    convert_pt_to_safetensors(args.input, args.output)
