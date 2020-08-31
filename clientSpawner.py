import os


def welcome():
    print("\nSpawning clients...\n\n")

    for x in range(10):
        x += 1
        os.system('python3 clientSocket.py ' + str(x))




if __name__ == "__main__":
    welcome()

