import json
from pathlib import Path
import argparse
import os

def get_nested_keys(d):
    if not d:
        return []

    keys = []
    for key, val in d.items():
        keys.append(key)
        keys.extend(get_nested_keys(val))
    return keys

parser = argparse.ArgumentParser()
parser.add_argument("--rec_dir", default="out", help="The directory where you store the scraped trees.")
parser.add_argument("--out_file", default="flatten_ids.txt", help="Txt file to store the flattened video ids.")

if __name__ == "__main__":
    args = parser.parse_args()
    files = [Path(args.rec_dir) / file for file in os.listdir(Path(args.rec_dir))]

    total_ids = []
    for file in files:
        with open(file) as f:
            tree = json.load(f)
        keys = get_nested_keys(tree)
        total_ids.extend(keys)
    
    unique_ids = list(set(total_ids))
    print(f"{len(unique_ids)} unique ids out of {len(total_ids)} total ids.")

    buffer = ""
    for id in unique_ids:
        buffer += id + "\n"
    
    with open(Path(args.out_file), "w") as f:
        f.write(buffer)
