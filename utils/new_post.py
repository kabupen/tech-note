from pathlib import Path
import os
import random
import hashlib
import subprocess

import argparse


def generate_hash():
    random_value = str(random.random()).encode("utf-8")
    hash_object = hashlib.sha256(random_value)
    return hash_object.hexdigest()[:14]


if __name__ == "__main__":
    hash_var = generate_hash()

    dir_name = f"src/content/blog/2025/11/{hash_var}/"
    index_path = Path(f"{dir_name}/index.mdx")
    print(">>>>", dir_name)
    os.makedirs(dir_name)
    index_path.touch()