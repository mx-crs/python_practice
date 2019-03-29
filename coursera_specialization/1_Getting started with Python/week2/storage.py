import os
import tempfile
import json
import argparse

storage_file = os.path.join(tempfile.gettempdir(), 'storage.data')

parser = argparse.ArgumentParser()
parser.add_argument('--key', '-key', dest='key')
parser.add_argument('--val', '-value', dest='val')
args = parser.parse_args()

val = None
if args.val:
    if args.val.isdigit():
        val = int(args.val)
    else:
        val = args.val

path_ex = os.path.exists(storage_file)

def create_json(path, key, val):
    with open(path, 'w') as f:
        storage = {key: [val]}
        json.dump(storage, f)

def add_to_json(path, key, val):
    with open(path, 'r') as f:
        storage = json.load(f)
        if key in storage and val not in storage[key]:
            storage[key].append(val)
        elif key not in storage:
            storage[key] = [val]
        with open(path, 'w') as f1:
            json.dump(storage, f1, indent=4)

def read_from_json(path, key):
    if os.path.exists(path):
        with open(path, 'r') as f:
            storage = json.load(f)
            if key in storage:
                print((', ').join(storage[key]))
    else:
        print(None)

if not val:
    read_from_json(storage_file, args.key)
elif path_ex:
    add_to_json(storage_file, args.key, val)
else:
    create_json(storage_file, args.key, val)