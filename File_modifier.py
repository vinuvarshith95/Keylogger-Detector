import time

while True:
    with open("testfile.txt", "a") as f:
        f.write("New data...\n")
    time.sleep(2)
