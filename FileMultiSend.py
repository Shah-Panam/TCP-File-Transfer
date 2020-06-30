import socket
import os
import tqdm

BUFFER_SIZE = 4096

s = socket.socket()
SEPARATOR = "<SEPARATOR>"

host = input("Enter Server IP Address: ")
port = 5001
filename = input("Enter name/ address of files to send. (Seperated by , ): ")
filenames = filename.split(",")
filesizes = []
totalsize = 0
for i in range(0, len(filenames)):
    filesizes.append(os.path.getsize(filenames[i]))
    totalsize = totalsize + filesizes[i]
print(totalsize)

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print(f"[+] Connected")
length = len(filenames)
print(length, totalsize)
s.sendall(f"{length}{SEPARATOR}{totalsize}".encode())

for i in range(0, length):
    s.send(f"{filenames[i]}{SEPARATOR}{filesizes[i]}".encode())
    confirm = s.recv(BUFFER_SIZE)
    #print(f"{filenames[i]}{SEPARATOR}{filesizes[i]}")

totalprogress = tqdm.tqdm(range(totalsize), f"Sending {length} files: ", unit="B", unit_scale=True, unit_divisor=1024)
for i in range(0, len(filenames)):
    BUFFER_SIZE = 4096
    progress = tqdm.tqdm(range(filesizes[i]), f"Sending {filenames[i]}: ", unit="B", unit_scale=True, unit_divisor=1024)
    # BUFFER_SIZE = filesizes[i]/100
    with open(filenames[i], "rb") as f:
        fsize = filesizes[i]
        while (fsize>0):
            bytes_read = f.read(BUFFER_SIZE)
            fsize -= len(bytes_read)
            if(fsize<BUFFER_SIZE):
                BUFFER_SIZE = fsize
                # print("Working?")
            if len(bytes_read) == 0:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            totalprogress.update(len(bytes_read))
            if(fsize == 0):
                confirm = s.recv(4096)
                break
            del bytes_read
        del progress
    f.close()
s.close()
