import re
import argparse

"""Implementing of basic functionality of os tool - grep."""

# Getting arguments and creating an usage message

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--exclusive", help="exclusive search", action="store_true")
parser.add_argument("pattern", help="pattern for search in file")
parser.add_argument("file", help="file name")
args = parser.parse_args()

# File opening and checking for existence and permissions of the file

try:
    file = open(args.file)
except (FileNotFoundError, PermissionError):
    print("There is a problem with file opening")
    exit(1)

# Process and printing the file line by line

while True:
    line = file.readline()
    if not line:
        break
    search_result = re.search(args.pattern, line)
    if (not args.exclusive and search_result or
            args.exclusive and not search_result):
        print(line, end='')
