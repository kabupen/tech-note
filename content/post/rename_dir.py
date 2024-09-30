import random
import hashlib
import glob
import subprocess

def generate_hash():
    random_value = str(random.random()).encode('utf-8')
    hash_object = hashlib.sha256(random_value)
    return hash_object.hexdigest()[:14]


save_dict = {}

for path in glob.glob("./*"):
    if path.endswith(".py") : continue
    if path.endswith(".pkl") : continue

    hash_var = generate_hash()

#     save_dict[path] = hash_var
    
    command = f"git mv {path} {hash_var}"
    print(command)
    subprocess.run([command,], shell=True)

# import pickle
# with open("savetmp.pkl") as f:
#     pickle.dump(f)

