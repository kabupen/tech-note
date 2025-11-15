import random
import hashlib
import subprocess

import argparse


def generate_hash():
    random_value = str(random.random()).encode("utf-8")
    hash_object = hashlib.sha256(random_value)
    return hash_object.hexdigest()[:14]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default="post")
    args = parser.parse_args()

    hash_var = generate_hash()

    if args.directory == "post":
        dir_name = f"post/{hash_var}/index.md"
    elif args.directory == "electrodynamics":
        dir_name = f"physics/electrodynamics/{hash_var}/index.md"
    elif args.directory == "mechanics":
        dir_name = f"physics/mechanics/{hash_var}/index.md"

    # print(f"post/{hash_var}/index.md")
    print(dir_name)

    subprocess.run([f"hugo new {dir_name}"], shell=True)
