import tempfile
import os


class File:

    """Creates iterable obj_file with supporting of __add__ and __repr__ method"""

    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        self.fd = open(self.file_path, 'r')
        return self

    def __next__(self):
        line = self.fd.readline()
        if not line:
            self.fd.close()
            raise StopIteration
        return line

    def __add__(self, obj):
        new_file = File(os.path.join(tempfile.gettempdir(), "add_file.txt"))
        new_file.write(self.read() + obj.read())
        return new_file

    def __repr__(self):
        return self.file_path

    def read(self):
        with open(self.file_path, 'r') as f:
            line = f.read()
        return line

    def write(self, line):
        with open(self.file_path, 'a') as f:
            f.write(line)