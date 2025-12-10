from datetime import datetime  
from pathlib import Path
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
    hash_var = generate_hash()

    today = datetime.now()
    year = today.year
    month = today.month  # 1〜12

    dir_name = f"src/content/blog/{year}/{month}/{hash_var}"
    index_path = Path(dir_name) / "index.mdx"

    print(">>>>", index_path)

    os.makedirs(dir_name, exist_ok=True)

    with index_path.open("w", encoding="utf-8") as f:
        f.write(FRONT_MATTER)
