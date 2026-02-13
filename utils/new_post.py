from datetime import datetime
from pathlib import Path
import argparse
import os
import random
import hashlib

def generate_hash():
    random_value = str(random.random()).encode("utf-8")
    hash_object = hashlib.sha256(random_value)
    return hash_object.hexdigest()[:14]


FRONT_MATTER = """---
title: ""
pubDate:
categories: [""]
tags: [""]
description: ""
---
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--study",
        nargs="?",
        const="physics/mechanics",
        help="Create a study note under src/content/study/<path> (default: physics/mechanics)",
    )
    args = parser.parse_args()

    hash_var = generate_hash()

    today = datetime.now()
    if args.study:
        study_path = args.study.strip("/").strip()
        dir_name = f"src/content/study/{study_path}/{hash_var}"
        index_path = Path(dir_name) / "index.mdx"
    else:
        year = today.year
        month = today.month  # 1〜12

        dir_name = f"src/content/blog/{year}/{month}/{hash_var}"
        index_path = Path(dir_name) / "index.mdx"
    front_matter = FRONT_MATTER

    print(">>>>", index_path)

    os.makedirs(dir_name, exist_ok=True)

    with index_path.open("w", encoding="utf-8") as f:
        f.write(front_matter)
