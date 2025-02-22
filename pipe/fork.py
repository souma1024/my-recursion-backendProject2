import os

r, w = os.pipe()
pid = os.fork()

if pid > 0:
    os.close(r)

    message = "Message from parent with pid {}".format(os.getpid())

    print("parent, sending out the message - {}".format(message, os.getpid()))

    os.write(w, message.encode("utf_8"))

else:
    os.close(w)
    print("Fork is 0, this is a child PID:", os.getpid())
    f = os.fdopen(r)
    print("Incoming string:", f.read())
