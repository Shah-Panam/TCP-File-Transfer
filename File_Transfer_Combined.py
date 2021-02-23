import socket
import os
import tqdm

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

choice= input("Enter Your Choice (send/receive/exit)")

while(choice != "exit"):
    if(choice == "send"):
        s = socket.socket()
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

    elif(choice == "receive"):
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

    elif(choice == "exit"):
        break

    choice= input("Enter Your Choice (send/receive/exit)")
os.system("pause")
