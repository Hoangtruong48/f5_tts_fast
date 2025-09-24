import torch
from safetensors.torch import load_file
import argparse


def convert_safetensors_to_pt(input_path, output_path):
    print(f"Loading safetensors file: {input_path}")
    state_dict = load_file(input_path)

    print(f"Saving as PyTorch checkpoint: {output_path}")
    torch.save({"model_state_dict": state_dict}, output_path)
    print("Conversion done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .safetensors to .pt")
    parser.add_argument("--from_path", type=str, required=True, help="Path to input .safetensors file")
    parser.add_argument("--to_path", type=str, required=True, help="Path to output .pt file")

    args = parser.parse_args()
    convert_safetensors_to_pt(args.from_path, args.to_path)
