import asyncio

class ServerError(Exception):
    pass

storage = dict()
clients = []

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print(f'Connected: {self.peername}')
        clients.append(self)

    def data_received(self, data):
        print(f"{self.peername} has sent {data.decode()}")
        resp = self.handle_data(data)
        print(f"Response to {self.peername}: {resp.decode()}")
        for client in clients:
            if client is self:
                client.transport.write(resp)

    def get_from_storage(self, key):
        acumm = ""
        if key == '*':
            for data in storage:
                for in_data in storage[data]:
                    acumm += f"{data} {in_data[0]} {in_data[1]}\n"
        elif key in storage:
            for data in storage[key]:
                acumm += f"{key} {data[0]} {data[1]}\n"
        return f"ok\n{acumm}\n"

    def handle_data(self, data):
        data_l = data.decode().split(' ')
        if data_l[0] != "get" and data_l[0] != "put":
            return f"error\n{data_l[0]}\n\n".encode("utf8")
        elif data_l[0] == "put":
            if len(data_l) != 4: raise ServerError
            if data_l[1] in storage and (float(data_l[2]), int(data_l[3].strip())) not in storage[data_l[1]]:
                storage[data_l[1]].append((float(data_l[2]), int(data_l[3].strip())))
            elif data_l[1] not in storage:
                storage[data_l[1]] = [(float(data_l[2]), int(data_l[3].strip()))]
            return "ok\n\n".encode("utf8")
        elif data_l[0] == "get":
            if len(data_l) != 2: raise ServerError
            data_l[1] = data_l[1].strip()
            if data_l[1] in storage or data_l[1] == '*':
                return self.get_from_storage(data_l[1]).encode()
            else:
                return "ok\n\n".encode("utf8")

    def connection_lost(self, ex):
        print(f"Disconnected: {self.peername}")
        clients.remove(self)

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
