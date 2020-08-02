import socket
import os
import tqdm
#asdsa
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
SERVER_HOST = input("Enter Your IP Address: ")
SERVER_PORT = 5001
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
CLIENT_SOCKET, address = s.accept()
print(f"[*] Connected with {address}")

received1 = CLIENT_SOCKET.recv(BUFFER_SIZE).decode()
length, totalsize = received1.split(SEPARATOR)
length = int(length)
print(length)
filenames = [None] * length
filesizes = [None] * length

for i in range(0, length):
    received = CLIENT_SOCKET.recv(BUFFER_SIZE).decode()
    CLIENT_SOCKET.send("Received".encode())
    filenames[i], filesizes[i] = received.split(SEPARATOR)
    filesizes[i] = int(filesizes[i])
    filenames[i] = os.path.basename(filenames[i])
# print(filesizes[1])
# print(filenames[1])
totalsize = int(totalsize)

totalprogress = tqdm.tqdm(range(totalsize), f"Receiving {length} files: ", unit="B", unit_scale=True, unit_divisor=1024)
for i in range(0, length):
    BUFFER_SIZE = 4096
    progress = tqdm.tqdm(range(filesizes[i]), f"Receiving {filenames[i]}: ", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filenames[i], "wb") as f:
        fsize = filesizes[i]
        while (fsize>0):
            bytes_read = CLIENT_SOCKET.recv(BUFFER_SIZE)
            fsize -= len(bytes_read)
            if(fsize<BUFFER_SIZE):
                BUFFER_SIZE = fsize
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
            totalprogress.update(len(bytes_read))
            if(fsize == 0):
                CLIENT_SOCKET.send(f"Done Sending".encode())
                break
            del bytes_read
        del progress
    f.close()
s.close()
