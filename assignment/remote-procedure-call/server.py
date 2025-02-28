import os, socket, math, json



class socket:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_address = '/tmp/server_socket_file' 
    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print('starting up on {}'.format(server_address))
    sock.bind(server_address)

    while True:
        print('\nwaiting to receive message')


class RpcFunction:
    def floor(x):
        return math.floor(x)
    
    def nroot(n, x):
        return math.log(x, n)

    def reverse(s):
        return s[::-1]
    
    def validAnagram(str1, str2):
        return sorted(str1) == sorted(str2)
    
    def sort(strArr):
        return sorted(strArr)