import time
import socket

class ClientError(Exception):
    pass

class Client:

    """A Client for receiving data from server"""

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    @classmethod
    def _convert_data(cls, string, metric):
        data = dict()
        string_s = string.split("\n")
        if "ok" in string and (metric in string or metric == '*'):
            string_s.pop(0)
            for line in string_s:
                line_s = line.split(' ')
                if len(line_s) == 3:
                    if line_s[0] in data:
                        data[line_s[0]].append((int(line_s[2]), float(line_s[1])))
                    else:
                        data[line_s[0]] = [(int(line_s[2]), float(line_s[1]))]
        elif "error" in string:
            raise ClientError
        return data

    def put(self, metric, val, timestamp=None):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            time_s = time.time() if timestamp is None else timestamp
            sock.sendall(f"put {metric} {val} {time_s}\n".encode("utf8"))
            response = sock.recv(1024)
            if response.decode("utf8") != "ok\n\n":
                raise ClientError

    def get(self, metric):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            sock.sendall(f"get {metric}\n".encode("utf8"))
            data = sock.recv(1024).decode("utf8")
            data = Client._convert_data(data, metric)
        return data
