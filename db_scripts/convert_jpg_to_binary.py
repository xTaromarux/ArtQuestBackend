import argparse
from pathlib import Path
import os
import shutil

def convert_jpg_to_bin(jpg_path, bin_path):
    with open(jpg_path, 'rb') as jpg_file:
        jpg_data = jpg_file.read()

    with open(bin_path, 'wb') as bin_file:
        bin_file.write(jpg_data)
        bin_file.flush()

def main():
    parser = argparse.ArgumentParser(description="This script converts jpg files into binary files.")
    parser.add_argument("--dict_name", type=str, help="Name of the directory containing *.jpg files.")
    parser.add_argument("--safe_mode", type=str, help="Enable safe mode (yes/no).")

    args = parser.parse_args()

    dict_name: str = args.dict_name
    passed_safe_mode = args.safe_mode
    is_safe_mode: bool
    if passed_safe_mode.lower() == "yes":
        is_safe_mode = True
    elif passed_safe_mode.lower() == "no":
        is_safe_mode = False
    else:
        print(f"Invalid argument --safe_mode={passed_safe_mode}.")
        return
        
    input_directory_path: Path = Path(os.path.join(Path(__file__).parent.resolve(), "images", dict_name))
    if not input_directory_path.exists() or not input_directory_path.is_dir():
        print(f"Directory does NOT exist. Path={input_directory_path}")
        return

    output_directory_path: Path = Path(os.path.join(Path(__file__).parent.resolve(), "images", f"binary_{dict_name}"))

    if output_directory_path.exists() and output_directory_path.is_dir() and not is_safe_mode:
        print("Directory already exists.")
        return
    elif output_directory_path.exists() and output_directory_path.is_dir() and is_safe_mode:
        try:
            shutil.rmtree(output_directory_path)
        except OSError as e:
            print(e)
            return
    else:
        print(123)
        os.mkdir(output_directory_path)

    for filename in os.listdir(input_directory_path):
        if filename.lower().endswith('.jpg'):
            jpg_path = os.path.join(input_directory_path, filename)
            bin_path = os.path.join(output_directory_path, f"{os.path.splitext(filename)[0]}.bin")
            convert_jpg_to_bin(jpg_path, bin_path)

if __name__ == "__main__":
    main()
