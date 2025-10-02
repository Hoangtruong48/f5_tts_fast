#!/usr/bin/env python3
import sys
import os
import torch
from safetensors.torch import save_file

def unwrap_state_dict(state_dict):
    """
    Đi sâu vào dict cho đến khi tất cả value đều là torch.Tensor.
    """
    if not isinstance(state_dict, dict):
        raise ValueError("Checkpoint không phải là dict hợp lệ")

    # Nếu value đầu tiên là tensor thì ok
    if all(isinstance(v, torch.Tensor) for v in state_dict.values()):
        return state_dict

    # Nếu có bọc thêm level, unwrap tiếp
    for key in ["state_dict", "model_state_dict", "model", "module"]:
        if key in state_dict and isinstance(state_dict[key], dict):
            return unwrap_state_dict(state_dict[key])

    # Nếu không tìm thấy thì báo lỗi
    raise ValueError("Không tìm thấy state_dict tensor trong checkpoint")


def convert_pt_to_safetensor(pt_path: str):
    if not os.path.isfile(pt_path):
        raise FileNotFoundError(f"Không tìm thấy file: {pt_path}")

    base, _ = os.path.splitext(pt_path)
    safetensor_path = base + ".safetensors"

    raw_state = torch.load(pt_path, map_location="cpu")
    state_dict = unwrap_state_dict(raw_state)

    save_file(state_dict, safetensor_path)
    print(f"✅ Đã convert {pt_path} -> {safetensor_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_pt_to_safetensor.py <model.pt>")
        sys.exit(1)

    pt_file = sys.argv[1]
    convert_pt_to_safetensor(pt_file)
