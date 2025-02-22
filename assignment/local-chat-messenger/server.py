import os, socket
from faker import Faker
fake = Faker()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/tmp/server_socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print("starting up on {}".format(server_address))
sock.bind(server_address)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)
    print('received {} bytes from {}'.format(len(data), address))

    data = data.decode()

    print(data)

    if "name" in data:
        sent = sock.sendto(fake.name().encode(), address)
        print('sent {} bytes back to 1\n{}'.format(sent, address))
        continue

    if "address" in data:
        sent = sock.sendto(fake.address().encode(), address)
        print('sent {} bytes back to 2\n{}'.format(sent, address))
        continue

    else:
        sent = sock.sendto(fake.text().encode(), address)
        print('sent {} bytes back to 3\n{}'.format(sent, address))