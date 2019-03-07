import os
import tempfile
import argparse
import json
import sys

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
parser = argparse.ArgumentParser()
parser.add_argument("--key", "-key_name", dest="key")
parser.add_argument("--val", "-value", dest="val")
args = parser.parse_args()

val = None
if args.val:
    if args.val.isdigit():
        val = int(args.val)
    else:
        val = args.val

key_val = [args.key, val]
out = []

try:
    with open(storage_path, 'r') as f:
        storage = json.load(f)
        if not args.val:
            for keyval in storage:
                if keyval[0] == args.key:
                    out.append(keyval[1])
            if not out:
                print(None)
            else:
                print(', '.join(out))
        else:
            for keyval in storage:
                if key_val == keyval:
                    sys.exit(0)
            storage.append(key_val)
            with open(storage_path, 'w') as f1:
                json.dump(storage, f1, indent=4)
except:
    if not val:
        print(None)
    else:
        with open(storage_path, 'w') as f:
            json.dump([[args.key, val]], f, indent=4)
